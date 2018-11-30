import re
import json
import socket
import lib.logger as logger
import urllib2
import time
import uuid
import os
from subprocess import check_output
from glob import glob
from datetime import datetime
from datetime import timedelta

SOURCE_ENV_CMD = '. /opt/datasynapse/*/work/$HOSTNAME-0/hadoop/rbs-env.sh'
DEFAULT_NAMENODE_HOST = os.environ['HOSTNAME'] #assume local
INCLUDE_FILENAME_TEST = '/tmp/hosts.include'
REFRESH_CMD = SOURCE_ENV_CMD + '; hdfs dfsadmin -refreshNodes' 
NAMENODE_PORT = 5070

#fsck
FILEREGEX = re.compile(r"(?P<fileName>/.*) (?P<bytes>\d+) bytes, (?P<blockCount>\d+) block\(s\): .*")
BLOCKREGEX = re.compile(r"(?P<blockNumber>\d+)\. (?P<BP>.+):(?P<blk>.+) len=(?P<len>\d+) repl=(?P<repl>\d+) \[(?P<ipstr>.*)\]")
BLOCKREGEX_MISSING = re.compile(r"(?P<blockNumber>\d+)\. (?P<BP>.+):(?P<blk>.+) len=(?P<len>\d+) (?P<error>.+)")
FSCK_CMD = SOURCE_ENV_CMD + '; hdfs fsck %s -files -blocks -locations'
DEFAULT_SLEEP_INTERVAL = 60 #secs
DEFAULT_TIMEOUT = DEFAULT_SLEEP_INTERVAL*20

'''
PRIVATE FUNCS
'''

def _getHostFromIP(ip):
    hostDetails = socket.gethostbyaddr(ip)
    host = hostDetails[0].split('.')[0]
    return host
    

def _callShell( cmd ):
    logger.info( 'running: %s', cmd )
    result = check_output( cmd, shell=True )
    return result

def _parseHostLine(hostList):
    result = hostList.split('#')[0].strip()
    return result


def _getJMXNameKey( rawKey ):
    res = dict( line.strip().split('=') for line in rawKey.split(',') )
    return res


def _getOrEnsureIsIP(host):
    strippedhost = host.strip()
    print strippedhost
    try:
        socket.inet_aton(strippedhost)
    except:
        strippedhost = socket.gethostbyname( strippedhost )
        logger.warn( '%s is not an IP address resolving to %s' % (host,strippedhost) )
    return strippedhost


def _updateHosts( srcFilename, updateFunc, *hosts, **kwargs ):
    '''
    kwargs
    debug - prints results
    targetFilename - defaults to filename
    '''
    if '*' in srcFilename: #assumes only 1 file to overwrite
        srcFilename = glob(srcFilename)[0]
        logger.warning( 'widlcard srcFilename input resolved to %s' % srcFilename )

    hostset = set( _getOrEnsureIsIP(s) for s in hosts) #ensure all IPs unique
    with open(srcFilename, 'r') as f:
        contents = f.readlines()
        contentsFiltered = set(_parseHostLine(x) for x in contents)

    result = list( updateFunc( contentsFiltered, hostset ) )
    result.sort()
    resultString = '\n'.join(result)

    if kwargs.get('debug', False):
        import StringIO

        output = StringIO.StringIO()
        output.write(resultString)
        #logger.debug(output.getvalue())
        outputString = output.getvalue()
        print( outputString )

    targetFilename = kwargs.get('targetFilename', srcFilename)

    with open(targetFilename, 'w') as f:
        f.write(resultString)

    #call hadoop command line to pick up changes
    _callShell( REFRESH_CMD )


def _getHostMetricsJMX(namenodeHost):
    rawData = urllib2.urlopen('http://%s:%s/jmx' % (namenodeHost,NAMENODE_PORT) ).read()
    jsonData = json.loads(rawData)
    return jsonData[ 'beans' ]


def _getHostMetricsJMXNameNode(namenodeHost):
    jsonData = _getHostMetricsJMX(namenodeHost)

    # jmxBeans = dict( zip( [ _getJMXNameKey( d['name'] ) for d in jsonData['beans'] ], jsonData['beans'] ) )
    # jmxBeans = jsonData['beans']
    nameNodeInfo = filter( lambda x: 'namenodeinfo' in x[ 'name' ].lower(),  jsonData )[0] # assuming only 1 element
    return nameNodeInfo


def _getNameNodeDir(namenodeHost):
    nameNodeInfo = nameNodeInfo = _getHostMetricsJMXNameNode(namenodeHost)
    nodeDirStatuses = json.loads( nameNodeInfo['NameDirStatuses'].decode('string_escape') )
    return nodeDirStatuses['active'].keys()[0]

'''
PUBLIC FUNCS
'''

def addHosts( srcFilename, *hosts, **kwargs ):
    '''
    Adds hosts ( as IP addresses ) to a file
    NOTE: this doesn't necessarily add them to the cluster e.g. adding hosts to the exclude list
    kwargs: see _updateHosts
    '''
    _updateHosts( srcFilename, set.union, *hosts, **kwargs)


def removeHosts( srcFilename, *hosts, **kwargs ):
    '''
    removes hosts ( as IP addresses ) to a file
    NOTE: this doesn't necessarily remove them to the cluster e.g. remove hosts from the exclude list
    kwargs: see _updateHosts
    '''
    _updateHosts( srcFilename, set.difference, *hosts, **kwargs)



def getAllNodeStatuses( namenodeHost ):
    '''
    Gets JMX details from NAMENODE given a hostname / ipaddress and returns datanode statuses
    TODO: refactor
    '''
    nameNodeInfo = _getHostMetricsJMXNameNode(namenodeHost)
    
    #construct dict of all nodes and append their status to each value.
    allNodeStatuses={}
    for k in [ 'DecomNodes', 'DeadNodes', 'LiveNodes' ]:
        nodeStatuses = json.loads( nameNodeInfo[k].decode('string_escape') )
        for nskey in nodeStatuses:
            nodeStatuses[ nskey ][u'status'] = k
        allNodeStatuses.update( nodeStatuses )

    return allNodeStatuses


def getNamenodeFromDatanode(hostname):
    #TODO: put in config, this logic is not stable
    if 'svsrs' in hostname:
        hostNumber = int( hostname.replace( 'svsrs', '' ) )
        result =  'svsrs00127' if hostNumber >= 138 else 'svsrs00126'
    elif 'svwrs' in hostname:
        hostname_replace = hostname.replace('svwrs', '')
        hostNumber = int(hostname_replace)
        result = 'svwrs00127' if hostNumber >= 138 else 'svwrs00126'
    else:
        raise RuntimeError('unknown hostname %s' % hostname )

    return result


def getNodeProperty( hostname, property, namenodeHost=None ):
    namenodeHost = namenodeHost or getNamenodeFromDatanode(hostname)
    nodeStatus = getAllNodeStatuses(namenodeHost)
    result = nodeStatus[ '%s.fm.rbsgrp.net' % hostname ][ property ]
    return result
    

def getNamenodeHostFileName( includeExclude, namenodeHostname=DEFAULT_NAMENODE_HOST ):
    '''
    includeExclude: 'include' or 'exclude' 
    '''
    return '%s/../hosts.%s' % ( _getNameNodeDir(namenodeHostname), includeExclude.lower() ) 


def waitForDatanodesStatusChange( status, *datanodeHostNames, **kwargs ):
    '''
    kwargs:
    sleepInterval: in secs
    namenodeHost: which namenode to get details from
    timeout: in seconds
    '''
    
    #setup timeout
    uid=uuid.uuid4() 
    timeout = kwargs.get('timeout', DEFAULT_TIMEOUT )
    expiry = datetime.utcnow() + timedelta( seconds=timeout )

    for datanode in datanodeHostNames:
        done = False
        while not done:
            #check for timeout
            if datetime.utcnow() > expiry:
               logger.warning( 'function timed out, terminating. timeout=%s uid=%s' % (timeout,uid)  )
               return
            
            #loop
            adminState = getNodeProperty(datanode, 'adminState', namenodeHost=kwargs.get('namenodeHost',None) )
            if adminState.lower() == status.lower() :
                logger.info( "DONE Datanode=%s finishedState='%s'. uid=%s" % (datanode, adminState, uid) )
                done = True
            else:
                sleepInterval = kwargs.get( 'sleepInterval', DEFAULT_SLEEP_INTERVAL )
                logger.info( "Waiting for status change. Datanode=%s currentState='%s' targetState='%s', sleeping for %ss uid=%s" % (datanode, adminState, status, sleepInterval, uid) )
                time.sleep( sleepInterval )

    logger.info( "All nodes done. finalState='%s' uid=%s" % (status,uid) )

	
def fsck( hdfsfilename=r'/', alreadyParsedFilename=None ):
    '''
    calls "hadoop fsck $hdfsfilename -files -blocks -locations" and parses results
    '''
    if alreadyParsedFilename:
        with open( alreadyParsedFilename, 'r' ) as f:
            resultArray = f.readlines()
    else:
        resultString = _callShell( FSCK_CMD % hdfsfilename )
        resultArray = resultString.split('\n')
		
    res = _parsefsck( resultArray )
    return res
   	
	
def _parsefsck( inputLines ):
	'''
	parses a "hadoop fsck / -files -blocks -locations" output
	inputLines must be an list of strings ( each new line as a separate element in list )
	'''
	result = {}
	currentdict = {'fileName': None}
	for l in inputLines:
		if ' bytes, ' in l:
			result[currentdict['fileName']] = currentdict
			match = re.search(FILEREGEX, l)

			currentdict = match.groupdict()
			currentdict['blocks'] = []

		elif 'len=' in l:
			match = re.search(BLOCKREGEX, l)
			if match:
				block = match.groupdict()
				block['ips'] = [ ip.split(':')[0] for ip in block['ipstr'].split(', ') ]
				block['hosts'] = [ _getHostFromIP(ip) for ip in block['ips'] ]
			else:
				match = re.search(BLOCKREGEX_MISSING, l)
				block = match.groupdict()

			currentdict['blocks'].append(block)
	
	# add last one
	result[currentdict['fileName']] = currentdict
	del result[None]
	return result
	
	
def _flattenfsck( dictOfFiles ):
    res = []
    for file in dictOfFiles.values():
        fileDetails = dict( (k,v) for k,v in file.iteritems() if k != 'blocks' )
        for block in file['blocks']:
            blockDetailsRaw = dict( (k,v) for k,v in block.iteritems() if k not in ['ips','hosts'] )
            blockAndFileDetails = dict( blockDetailsRaw, **fileDetails )
            for i in range( len(block[ 'ips' ]) ):
                allDetails = dict( blockAndFileDetails, **{
                    'ip': block[ 'ips' ][i],
                    'host': block[ 'hosts' ][i],
                    'blockOrder': i,
                } )
                res.append( allDetails )
   
    return res                     
    
