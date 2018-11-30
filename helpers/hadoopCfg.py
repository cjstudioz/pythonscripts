_drDatanodes = map( lambda x: 'svwrs00%s' % str(x).zfill(3), range(138,229) )
_prodDatanodes = map( lambda x: 'svsrs00%s' % str(x).zfill(3), range(138,229) )
_devDatanodes = map( lambda x: 'svwrs00%s' % str(x).zfill(3), range(1,92) )
_uatDatanodes = map( lambda x: 'svsrs00%s' % str(x).zfill(3), range(1,92) )

CLUSTERS = {
    'prod': {
        'namenodes': [ 'svsrs00127', 'svsrs00133' ],
        'datanodes': _prodDatanodes,
    },
    'dr': {
        'namenodes': [ 'svwrs00127', 'svwrs00133', 'svwrs00261', 'svwrs00262' ],
        'datanodes': _drDatanodes,
    },
    'uat': {
        'namenodes': [ 'svsrs00126', 'svsrs00132' ],
        'datanodes': _uatDatanodes,
    },
    'dev': {
        'namenodes': [ 'svwrs00126', 'svwrs00132' ],
        'datanodes': _devDatanodes,
    },       
}
    
