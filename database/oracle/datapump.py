import re
from database.oracle.core import getConnDetails
from helpers.datetime import nowStr
from helpers.platform import isWindows

WHITESPACE = re.compile(r'\s+')
LINUXESCAPE = re.compile(r'([\'()])')
       

IMPDP_PARAMS = {
    'CJCORE': dict(
        directory='CUTDOWN_DIR',
        #schemas='CJCORE',
        parallel=8,
        exclude='USER,TABLE_STATISTICS',
        remap_schema=WHITESPACE.sub('', '''
            CJCORE:{user},
            CJCORE_RO:{user}_RO,
            CJWI:CJWI{usersuffix},
            CJODM:CJODM{usersuffix},
            CJEST:CJEST{usersuffix},
            APP_BASE:APP_BASE{usersuffix},
            RO_BASE:RO_BASE{usersuffix},
            RO_CJCORE:RO_CJCORE{usersuffix},
            RO_CJWI:RO_CJWI{usersuffix},
            APP_CJCORE:APP_CJCORE{usersuffix},
            APP_CJODM:APP_CJODM{usersuffix},
        '''),
        remap_tablespace=WHITESPACE.sub('', '''
            CJCORE_DAT:CJCORE51_DAT,
            CJCORE_IDX:CJCORE51_IDX,
            CJCORE_LOB:CJCORE51_LOB        
        '''),
                 
    ),
    
    'CJCORE_HK': dict(
        directory='EXPORT_DIR',
        #schemas='CJCORE',
        parallel=8,
        exclude='USER,TABLE_STATISTICS,OBJECT_GRANT,ROLE_GRANT',
        remap_schema='CJCORE:{user}',
        remap_tablespace=WHITESPACE.sub('', '''
            CJCORE_DAT:USER_DATA,
            CJCORE_IDX:USER_DATA,
            CJCORE_LOB:USER_DATA        
        '''),              
    ),
                                        
    'JAVA_HK': dict(
        directory='EXPORT_DIR',     
        remap_schema='CJCORE:{user}',
    )
}

def _linuxify(cmd):
    """
    TODO: better way to escape linux chars? shlex and re.escape don't cover it
    """
    return LINUXESCAPE.sub(r'\\\1', cmd)
    

def impdpCmd(
    user,
    db,
    dumpfile, 
    paramCfg='CJCORE_HK',
    **overrides
):
    """
    builds command for Oracle datapump import. requries thick client on the hsot this sCJipt runs from
      
    """
    connDetails = getConnDetails(user, db)
    defaultfict = IMPDP_PARAMS.get(paramCfg, {})
    params = dict(defaultfict, **overrides)
    params['dumpfile'] = dumpfile
    params['logfile'] = dumpfile.lower().replace('.dmp', '%s_%s.log' % (nowStr(), user))
    paramsStr = ' '.join('%s=%s' % kv for kv in params.items()).format(**locals()) 
    
    cmd = 'impdp {0}/{1}@{2} {paramsStr}'.format(*connDetails, **locals()).replace('\n', ' ')
    
    #escape if linux
    if not isWindows():
        cmd = _linuxify(cmd)
    
    return cmd


def datapumpPredicate(predicates, objType='TABLE'):
    """
    generates a filter CJiteria for datapump
    e.g. exclude:TABLE:\"LIKE 'SRC%'\"
    assumes predicate's column name is empty string ''
    """
#    quoteChar = r'\"'# if isWindows() else r'"'
#    localsVars = locals()
#    return ['{objType}:{quoteChar}{0}{quoteChar}'.format(pred.get_sql().strip(), **localsVars) for pred in predicates] #with_quotes=False
#    
    return [r'%s:\"%s\"' % (objType, pred.get_sql().strip()) for pred in predicates] #with_quotes=False
    

############################TESTS############################

def impdpTest():
    from database.oracle.datapump import impdpCmd
    user = 'CJCORE'
    db = 'CJDB'
    dumpfile = 'CJCORE_PROD_ME_20170102_%U.dmp'
    cmd = impdpCmd(user, db, dumpfile)
    #!{cmd}
    
    cmd = impdpCmd(user, db, 'java.dmp', defaults={}, 
        directory='EXPORT_DIR',     
        remap_schema='CJCORE:' + user,               
    )
