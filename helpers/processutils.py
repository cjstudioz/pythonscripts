import os
import lib.logger as logger
from threading import Timer
from contextlib import contextmanager
from lib.contexthelper import Timeit
from subprocess import Popen, PIPE, CalledProcessError, check_output

WINDOWS_SLEEP_CMD='ping 1.1.1.1 -n 1 -w 3000'

@contextmanager
def change_working_dir( working_dir ):
    #does nothing if working_dir is None
    if working_dir:
        old_dir = os.getcwd()
        try:
            os.chdir(working_dir)
            yield
        finally:
            os.chdir(old_dir)
    else:
        yield


def _create_piped_input( input_string ):
    if( input_string ):
        unused, inpipe = os.pipe()
        os.write( inpipe, input_string )
        return inpipe
    else:
        return None

def log_subprocess_cmd( args ):
    cmd = args if type(args) == "str" else " ".join(args)
    logger.info("running: %s" % cmd)


def run_cmd( args, #String or Array
             working_dir=None,
             stdin_string=None,
             ):
    stdin = _create_piped_input(stdin_string)
    with change_working_dir(working_dir):
        log_subprocess_cmd(args)
        output = check_output(args, shell=True, stdin=stdin )

    return output

def run_cmd_incremental( args, #String or Array
                         working_dir=None,
                         bytes_to_read_per_poll = 1000000 #arbitrary number
                         ):
    with change_working_dir(working_dir):
        log_subprocess_cmd(args)
        err = ""

        p = Popen(args, stdout=PIPE, stderr=PIPE, shell=True)

        while True: #mimic do while control structure
            stdout, stderr = p.stdout.read(bytes_to_read_per_poll), p.stderr.read(bytes_to_read_per_poll)

            #store off all stderr in case process ends in errorcode
            if stderr:
                err += stderr

            #return stdout and stderr so far
            if stdout or stderr:
                yield stdout, stderr

            if p.poll() is not None:
                break

        if p.returncode:
            raise CalledProcessError(p.returncode, args, err)


def run_cmd_get_output( args, #String or Array
                        working_dir=None,
                        log=False,
                        ):
    result_stdout = ""
    result_stderr = ""

    for stdout, stderr in run_cmd_incremental(args, working_dir):
        if stdout:
            result_stdout += stdout
            if log:
                logger.info("  {stdout}")
        if stderr:
            result_stderr += stderr
            if log:
                logger.error("  {stderr}")

    return result_stdout, result_stderr



def timedSubprocess( timeout, *args, **kwargs):
    '''
    subprocess.check_output with timeout
    *args and *kwargs for Popen
    kwarg timeoutmsg: logged as error if process times out
    returns tuple ( execution clocktime, Popen object )
    '''
    timeoutmsg = kwargs.get('timeoutmsg' )or '%s timed out after %ss' % ( args, timeout )
    
    def killProcess():
        p.kill() 
        logger.error( timeoutmsg )    
    
    with Timeit() as timed:
        p = Popen(*args, **kwargs)
        t = Timer( timeout, killProcess )
        t.start()
        p.wait()

    t.cancel()
    return timed.elapsed, p







