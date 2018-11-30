from sqlalchemy import *
from sqlalchemy.sql import select, expression
from sqlalchemy.sql.expression import Executable, ClauseElement
from sqlalchemy.ext.compiler import compiles
from dicthelper import rename_keys
from datetime import datetime
import string


def _get_non_whitespace_map( listofstrings ):
    listofstringswithoutspaces = [ string.replace( key, " ", "_") for key in listofstrings ]
    return dict(zip(listofstrings, listofstringswithoutspaces))


def _infer_columns_from_table(array_dicts):
#    if array_dicts.count <= 0:
#        raise
    columns = []
    for key, val in array_dicts[0].iteritems():
         try:
             int(val)
             type = Integer
         except:
             try:
                 float(val)
                 type = Float
             except:
                 type = String

         columns.append( Column( key, type ) )

    return columns

def _insert_table( resulttable, array_dicts, metadata, columns, indexes ):
    if isinstance(resulttable, Table):
        raise Exception('Not yet implemented use string tablename instead')

    elif isinstance(resulttable, basestring):
        cols_and_indexes = columns + indexes
        newtable = Table(resulttable, metadata, *cols_and_indexes, keep_existing=True )

    newtable.create(checkfirst=True)
    insertstatement = newtable.insert()
    metadata.bind.execute(insertstatement, array_dicts)
    return newtable


def insert_array_dicts_into_table( tablename, array_dicts, metadata, indexes=[], substitute_white_space=True ):
    if substitute_white_space:
        keys_with_spaces = [ key for key in array_dicts[0].keys() if " " in key ]
        rename_map = _get_non_whitespace_map( keys_with_spaces )
        for row in array_dicts:
            rename_keys(row, rename_map, ignore_missing_keys=True)

    columns = _infer_columns_from_table(array_dicts)
    newtable = _insert_table( tablename, array_dicts, metadata, columns, indexes )
    return newtable


def insert_resultProxy_into_table( tablename, rowset, metadata, indexes=[] ):
    columns = [coltuple[1][0].copy() for coltuple in rowset.context.result_map.values()]
    rows_to_insert = [ dict(zip( row.keys(), row )) for row in rowset ]
    newtable = _insert_table( tablename, rows_to_insert, metadata, columns, indexes )
    return newtable

def sqlite_date_diff( uppercol, lowercol, lablename, multiplier=24 ):
    ''' diff in hours by default
    '''
    return r'( julianday(%s) - julianday(%s) ) * %s as %s' % (uppercol, lowercol, multiplier, lablename )


def get_date_format():
    return '%Y-%m-%d %H:%M:%S'


def datetime_to_string(dateelement): #add dialects here as more and more
    datetimeformat = get_date_format()

    if isinstance( dateelement, datetime ):
        return dateelement.strftime(datetimeformat)
    elif isinstance( dateelement, basestring ):
        return dateelement
    else:
        raise TypeError('func expects string or datetime')

def get_drop_table_sql(
    table_name,
    type='Oracle'
):
    result = {
      'Oracle':
            '''
            Begin
               Execute Immediate 'truncate Table {table_name}';
               EXECUTE IMMEDIATE 'Drop Table {table_name}';
            EXCEPTION
               WHEN OTHERS THEN
                  IF SQLCODE != -942 THEN
                     RAISE;
                  End If;
            End;
            '''.format( **locals() )
    }[type]

    return result

if __name__ == "__main__":
    engine = create_engine('sqlite:///:memory:')
    array_dicts = [ {"sdfsd sdfs ":1, "a":5.0}, {"sdfsd sdfs ":2, "a":4.0} ]
    res = array_dicts_to_table( "mytable", array_dicts, engine )
    print res

