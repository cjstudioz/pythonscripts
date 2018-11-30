from splunklib import client, results
from lib.urllibUtils import callWebAPI
import json

SPLUNK_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

SPLUNK_INSTANCES = {
    'local': {
        'host': 'localhost',
        'port': 8089,
        'username': 'admin',    
        'password': 'admin',
    },
    'accelerate': {
        'host': 'lonrs07910',
        'port': 8089,
        'username': 'rest',    
        'password': 'X6zxX0UpUD',
    },
    'prod': {
        'host': 'lonrs09181',
        'port': 8089,
        'username': 'rest',    
        'password': 'X6zxX0UpUD',
    },
    'uat': {
        'host': 'lon0276xus',
        'port': 8089,
        'username': 'rest',    
        'password': 'X6zxX0UpUD', 
    },
    
}

DEFAULT_WEB_PARAMS = {
    'output_mode': 'csv', #json
    'field_list': '_time,_raw',
    'count': 50000, #max number of events from limits.conf TODO: anyway to infer this from a query?
}

def _getDateTimeString( datetime ):
	result = datetime if type(datetime) == str else datetime.strftime( SPLUNK_DATETIME_FORMAT )
	return result


def _getService( env ):
	'''
	change this to local environment
	'''
	
	kwargs = SPLUNK_INSTANCES[ env ] if type(env) == str else env
	return client.connect( **kwargs )

	   
def querySplunk( query, env, earliest_time='-365d', latest_time='now', count=9999999 ):
    service = _getService(env)
    job = service.jobs.oneshot( query, 
        earliest_time=_getDateTimeString(earliest_time),
        latest_time=_getDateTimeString(latest_time),
        count = count,
    )
    reader = results.ResultsReader( job )
    return reader


def restGetApps( splunkinstance ):
    env = dict( SPLUNK_INSTANCES[ splunkinstance ])
    searchurl = r'https://{host}:{port}/services/apps/local'.format( **env )
    res = callWebAPI( searchurl, env['username'], env['password'], 'get', { 'output_mode': 'json' } )                   
    js = json.loads( res )  
    return js
      

def restGetAppNames( splunkinstance ):
    js = restGetApps( splunkinstance )
    result = map( lambda x: x['name'], js[ 'entry' ] )
    return result

def restQuery( searchString, splunkinstance, app, maxRows=150000, webqueryparams=DEFAULT_WEB_PARAMS ):    
    
    #url = r'https://lonrs07910:8089/servicesNS/leecaf/search_accelerate/search/jobs/oneshot?output_mode=csv&field_list=_raw,_time&offset=900&count=999&search=|savedsearch "temp namenode"'
    #url = r'https://admin:HPCT3am@lonrs07910:8089/servicesNS/nobody/search_accelerate/search/jobs/oneshot?output_mode=json&search=|savedsearch "HDFS read stats"'
    #res = urllib2.urlopen( url ).read()
    
    #setup
    searchString = searchString if searchString.startswith('search ') else "search " + searchString
    env = dict( SPLUNK_INSTANCES[ splunkinstance ], app=app )
    
    #prepare query and run once
    searchparams = {
        'output_mode': 'json', #json
        'exec_mode': 'blocking',
        'search' : searchString, #r"search index=hadoop sourcetype=namenode", #r'|savedsearch "temp namenode"',
    }
    searchurl = r'https://{host}:{port}/servicesNS/{username}/{app}/search/jobs'.format( **env )  #% urllib.urlencode(params)    
    res = callWebAPI( searchurl, env['username'], env['password'], 'post', searchparams )                   
    js = json.loads( res )    

    #get SID for querying data    
    sid = js['sid']
    
    #iteratively collect results 50k events at a time
    results = []
    offset = 0
    retrieveurl = r'%s/%s/results' % (searchurl,sid)
    while True:
        retrieveparams = dict( webqueryparams, offset=offset )         
        res = callWebAPI( retrieveurl, env['username'], env['password'], 'get', retrieveparams )  
        results += res.split('\n')[:-1]                 
        offset += webqueryparams[ 'count' ]
        if offset >= maxRows:
            break 
            
    return results        
    

