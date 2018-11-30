import os
from lib.contexthelper import ignore_exception
import lib.logger as logger
import shutil
from subprocess import Popen, check_output

logger = getlogger()

__all__ = ["copy", "move", "remove", "copytree_overwrite" ]

def copytree_overwrite( src, dst ):
    if os.path.isdir( dst ):
        remove( dst )
    shutil.copytree(src, dst)


def copy(src, dst):
    logger.debug("copying %s %s" % (src, dst))
    if os.path.isfile(src):
        shutil.copy(src, dst)
    elif os.path.isdir(src):
        copytree_overwrite(src, dst)
    else:
        raise Exception("unexpected file type to copy %s" % src)


def move(src, dst):
    logger.debug("moving %s to %s" % (src, dst))
    if os.path.exists(src):
        os.rename(src, dst)
    else:
        logger.debug("%s does not exist" % src)


def remove(filename):
    logger.debug("deleting %s" % filename)
    if os.path.isfile(filename):
        os.remove(filename)
    elif os.path.isdir(filename):
        from shutil import rmtree
        rmtree(filename)


def find_file_handles( filestring, outildir='d:/outils' ):
    '''
        Requires outils, which is installed on all servers but not user desktops
    '''
    cmd = os.path.join( outildir, r'handle /accepteula %s' % filestring )
    logger.debug( 'running: %s' % cmd )
    try:
        res = check_output(cmd, shell=True)

    except:
        logger.debug( 'no processes found' )
        return None

    res_split = res.split('\n')
    filtered_res = [ x for x in res_split if 'pid' in x ]
    return filtered_res




