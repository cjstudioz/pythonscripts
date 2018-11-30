from splunklib import client, results
from lib.splunkUtils import SPLUNK_INSTANCES, querySplunk

additionalArgs = {
    'app': 'SplunkDeploymentMonitor',
}

env = dict( SPLUNK_INSTANCES[ 'accelerate' ], **additionalArgs )
query = 'search `all_forwarders`'
query = r'|savedsearch  "All forwarders"'
reader = querySplunk(query, env, earliest_time='-3d', latest_time='now' )
listOfDicts = [ dict(x) for x in reader ]
hosts = set( x['sourceHost'] for x in listOfDicts )


# Compare against predefined hosts
otherHosts = set( x.strip() for x in '''
# silver fabric Coherence
lonrs09173
lonrs09047
lonrs09047
lonrs09173
lonrs07988
lonrs09174
lonrs09174

# silver fabric Hadoop
lonrs09720
lonrs09720
lonrs09024
lonrs03255
lonrs03255
lonrs09024

# grid server
# lonrs07988

'''.split( "\n" ) if '#' not in x and x.strip() != '' )

svwrs = set( 'svwrs' + str(x).zfill(5) for x in xrange(1, 260+1 ) )
svwrsexclude = set( 'svwrs' + str(x).zfill(5) for x in xrange(229, 254+1 ) )
svwrsexclude2 = set( 'svwrs' + str(x).zfill(5) for x in xrange(92, 125+1 ) )

svsrs = set( 'svsrs' + str(x).zfill(5) for x in xrange(1, 280+1 ) )
svsrsexclude = set( 'svsrs' + str(x).zfill(5) for x in xrange(229, 274+1 ) )
svsrsexclude2 = set( 'svsrs' + str(x).zfill(5) for x in xrange(92, 125+1 ) )

allhosts = set.union( svwrs, svsrs, otherHosts )

diff = sorted(list(allhosts - hosts - svwrsexclude - svsrsexclude - svsrsexclude2 - svwrsexclude2 ))
print diff