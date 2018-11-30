import easygui as eg

INPUT_FIELDS = [ 'date', 'steps', 'interval' ]
#DEFAULT_INTPUTS=[ date.today().strftime(TIME_FORMAT), 4, 2000 ]


inputs = eg.multenterbox( title='select country', 
    fields=INPUT_FIELDS, 
    #values=DEFAULT_INTPUTS,
)

print inputs