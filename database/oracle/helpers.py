from pypika import Query as q, Field as f
from functools import lru_cache


def getTablesWithColsQry(colNames, schema=None):
    """
    
    :param list/str colNames:
    :param database.oracle.OraConnection conn: 
        
    Example usage:
    colNames = ['col1']    
    schema = 'myuser'
    """
    if isinstance(colNames, str): #takes str or list
        colNames = [colNames] 
    
    query = q().from_(
        'ALL_TAB_COLUMNS'
    ).distinct().select(
        'TABLE_NAME'
    ).where(
        f('COLUMN_NAME').isin(colNames)
    )
    
    if schema:
        query = query.where(f('OWNER') == schema)
    
    res = query.get_sql() #with_quotes=False)
    return res

@lru_cache()
def getTablesWithCols(conn, colNames, **kwargs):
    """
    
    :param dict kwargs: see getTablesWithColsQry
    :returns pandas.Series:
    """
    sql = getTablesWithColsQry(colNames, **kwargs)
    df = conn.getdf(sql)
    return df.ix[:,0]


def createViewsFromAnotherSchema(tables, srcSchema):
    localVars = locals()
    sqls = ["create or replace view {0} as select * from {srcSchema}.{0}".format(table, **localVars) for table in tables]
    return sqls


def grantTables(tables, user='PUBLIC', priv='select'):
    localVars = locals()
    sqls = ["grant {priv} on {0} to {user}".format(table, **localVars) for table in tables]
    return sqls 

################################### TEST #######################

def testGetTablesWithCols():
    from database.oracle.helpers import getTablesWithCols
    from database.oracle.core import connect
    conn = connect()
    getTablesWithCols(conn, 'CALC_SYSTEM_DATE')
