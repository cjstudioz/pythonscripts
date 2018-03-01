import cx_Oracle
import logging
import pandas as pd
from functools import lru_cache

# DB hosts - add more if nedded 
DBS = dict(
    CJDB = 'host:port/sid',    
)

PWS = dict(
    COMMON = {
      'mylogin': 'myPassword',                   
    },
    CJDB={    
      'mylogin': 'myPassword2',  
    },
)
       

def dateToOraStr(dt):
    return dt.strftime('%d-%b-%Y')
    
def connectRaw(*args):
    return OraConnection(cx_Oracle.connect(*args))
    
def getConnDetails(user, dbalias, passwd=None):
    pw = passwd or PWS.get(
        dbalias, {}
    ).get(user, 
        PWS['COMMON'].get(user, user)
    )
    return (user, pw, DBS[dbalias])    
    
def connect(user, dbalias, passwd=None):    
    args = getConnDetails(user, dbalias, passwd)
    logging.debug('connecting to: %s' % str(args))
    return connectRaw(*args)        

class OraConnection(object):
    """
    Additional helper functions
    """
    logger = logging.getLogger() #('OraConnection') TODO: find proper way to log
    
    def __init__(self, conn):
        self.conn = conn
        self.id = '%s@%s' % (self.conn.username, self.conn.tnsentry)
    
    @lru_cache()
    def getcursor(self):
        return self.conn.cursor()
    
            
    def execute(self, sql, verbose=True):
        """
        wrapper with extra logging
        """
        self.logger.info(sql + ' <db> %s' % self.id)
        return self.getcursor().execute(sql)
    
        
    def executeMany(self, sqls):
        if isinstance(sqls, str):
            sqls = filter(None, [s.strip() for s in sqls.split(';')])
                    
        for sql in sqls:
            if not sql.startswith('--') or ('\n' in sql): #avoid executing comment only lines
                self.execute(sql)
   
    def getdf(self, sql, **kwargs):
        self.logger.info('get dataframe: %s <db> %s' % (sql, self.id))
        return pd.read_sql(sql, self.conn, **kwargs)
