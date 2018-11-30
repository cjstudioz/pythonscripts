import traceback
import sys
from StringIO import StringIO
from contextlib import contextmanager
import lib.logger as logger
from StringIO import StringIO
import logging
from timeit import default_timer

@contextmanager
def logToStringIO():
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    rootlogger = logging.getLogger()
    rootlogger.setLevel(logging.INFO)
    rootlogger.addHandler(handler)
    yield stream
    handler.flush()
    rootlogger.removeHandler(handler)

@contextmanager
def ignore_exception( msg='' ):
    if msg:
        logger.info(msg)
    try:
        yield
    except Exception, excmsg:
        logger.warning(excmsg)
        traceback.print_exc(file=sys.stdout)

@contextmanager
def capture_stdout():
    '''
    Mainly used for test to check stdout contains expected strings
    Todo: does not work for functions that write to filestream directly e.g. logging.logger module
    '''

    saved_stdout = sys.stdout
    out = StringIO()
    try:
        sys.stdout = out
        yield out
    finally:
        sys.stdout = saved_stdout


@contextmanager
def capture_stderr():
    '''
    Mainly used for test to check stdout contains expected strings
    Todo: does not work for functions that write to filestream directly e.g. logging.logger module
    '''

    saved_stderr = sys.stderr
    out = StringIO()
    try:
        sys.stderr = out
        yield out
    finally:
        sys.stderr = saved_stderr
        

class Timeit(object):
    def __init__(self):
        self.timer = default_timer
        
    def __enter__(self):
        self.start = self.timer()
        return self
        
    def __exit__(self, *args):
        end = self.timer()
        self.elapsed = end - self.start
