#!/usr/bin/env python
# coding=utf-8

"""Data manipulation and cost allocation helpers."""

import pandas as pd
import numpy as np
import sqlalchemy as sa
import logging
import re

def getEngine(*args, **kwargs):
    engine = sa.create_engine('oracle+cx_oracle://localhost', *args, **kwargs)
    return engine

def insertDFOra(tablename, df, engine):
    """
    inserts panda datafrom into an oracleDB
    pandas.Dataframe.to_csv is too slow for Oracle
    NOTE:
        1. converts cols to lowercase so they're not case sensitive in ORA.
        2. only
    """
    if not len(df):
        logging.warning('nothing to insert into %s' % tablename)
        return

    proxy = engine.execute('select * from %s where 1=0' % tablename)  # get column names from DB
    renamed = df.rename(columns=dict(zip(  # sqlalchemy makes any string with upper case case sensitive
        df.columns,
        map(str.lower, df.columns)
    )))
    commonCols = list(
        set(proxy.keys()).intersection(set(renamed.columns))
    )
    proxy.close()
    if not commonCols:
        raise RuntimeError('no common columns found with %s' % tablename)


    subdf = renamed[commonCols]  # only insert cols which exist in target table

    #Correct String cols from NaN to Nones
    pandasengine = pd.io.sql.pandasSQL_builder(engine)
    table = pd.io.sql.SQLTable(tablename, pandasengine, df, index=False)
    cols, data_list = table.insert_data()
    rows = zip(*data_list)
    data = [dict((k, v) for k, v in zip(cols, row)) for row in rows]

    colnames = ', '.join(commonCols)
    params = ', '.join([':%s' % col for col in commonCols])
    sql = "insert /*+ append */ into {tablename} ({colnames}) values ({params})".format(**locals())
    #data = subdf.to_dict('records') #as list of dicts

    logging.info('inserting into %s %s rows with cols: %s' % (tablename, len(data), colnames))
    engine.execute(sql, data)

    # dataframe.to_csv is too slow
    #subdf.to_sql(tablename, engine,
    #     if_exists='append',
    #     index=False,
    # )

def getOraDtypeOverrides(df):
    stringCols = [k for k, dtype in df.dtypes.to_dict().iteritems() if dtype == np.dtype('object')]
    dtypeOverrides = {col: sa.types.VARCHAR(df[col].str.len().max()) for col in stringCols}
    #dtypeOverrides = {col: sa.types.VARCHAR(1024) for col in stringCols}
    return dtypeOverrides

def curateCol(col):
    return re.sub(r'[/()-:\\&\\S\\% ]+', '_', col.lower())[:30]
            
                                          

def createTableOra(tablename, df, engine):
    """
    df = pd.read_csv(r'c:/ubs/dev/models/masterdata/clean/model_configuration__job_map_xl.txt')
    createTableOra('static_job_map', df, engine)
    """
    dtypeOverrides = getOraDtypeOverrides(df)
    pandasengine = pd.io.sql.pandasSQL_builder(engine)
    table = pd.io.sql.SQLTable(tablename, pandasengine, df, index=False, dtype=dtypeOverrides)
    table.create()

if __name__ == '__main__':
    pass

