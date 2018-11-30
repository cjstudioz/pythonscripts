from itertools import repeat
from datetime import datetime
from dateutil import *

_datetime_args_sequence = [ 'year', 'month', 'day', 'hour', 'minute', 'second' ]

def floor(
    datetimeobj,
    round_to, #valid inptus are in _datetime_args_sequence
):
    if round_to not in  _datetime_args_sequence:
        raise ValueError( 'invalid round_to input %s, valid inputs are %s' % ( round_to, _datetime_args_sequence ))

    args = []
    for timeunit in _datetime_args_sequence:
        args.append( datetimeobj.__getattribute__(timeunit) )
        if timeunit == round_to:
            arglength = len(args)
            if arglength < 3 : # datetime requires at least input up til days
                filler = [ 1 for unused in range(3-arglength)]
                args += filler #appened blank month and day if necessary
            return datetime( *args )



