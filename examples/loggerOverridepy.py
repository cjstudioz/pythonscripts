import logging

class MyHandler(logging.Handler): # Inherit from logging.Handler
        def __init__(self):
                # run the regular Handler __init__
                logging.Handler.__init__(self)
                
        def emit(self, record):
                # record.message is the log message
                print(dir(record))


# handlertest.py
import logging
import logging.handlers

logger = logging.getLogger()

# A little trickery because, at least for me, directly creating
# an SMSHandler object didn't work
logging.handlers.MyHandler = MyHandler

# create the handler object
testHandler = logging.handlers.MyHandler()

# and finally we add the handler to the logging object
logger.addHandler(testHandler)

# And finally a test
logger.debug('Test 1')
logger.info('Test 2')
logger.warning('Test 3')
logger.error('Test 4')
logger.critical('Test 5')