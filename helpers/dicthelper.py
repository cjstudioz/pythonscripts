from csv import DictWriter
from collections import OrderedDict

def apply_on_subset( d, keys, modifyfunc ):
    for key in keys:
        d[ key ] = modifyfunc( d[ key ] )


def rename_keys( d, keys_map, ignore_missing_keys=False ):
    for key, newkey in keys_map.iteritems():
        if not ignore_missing_keys or d.has_key( key ):
            d[newkey] = d[key]
            del d[key]

def subdict( d, keys ):
     return OrderedDict((k, d[k]) for k in keys if k in d)

def to_csv( list_of_dicts, filename, writeheader=True ):
    ''' unordered keys
    '''
    with open( filename, 'wb' ) as file:
        mycsv = DictWriter( file, list_of_dicts[0].keys() )
        if writeheader:
            mycsv.writeheader()
        mycsv.writerows( list_of_dicts )
