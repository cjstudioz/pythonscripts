from exceptions import Exception
import lib.logger as logger
import re
from processutils import run_cmd_get_output
import os
import lib.winregutils


#private variables
_java_version_regex = re.compile("version \"(.*)\"", re.IGNORECASE)
_java_bit_arch_regex = re.compile("(\d*)" + re.escape("-bit"), re.IGNORECASE)

def _get_java_path_from_env_var_if_none(java_path):
    #dont set default in definitn as os.environ['JAVA_HOME'] may be changed just before fn call
    if not java_path:
       java_path = os.environ['JAVA_HOME'] + r'\bin\java'
    return java_path

def get_java_details( java_path=None ):

    java_path = _get_java_path_from_env_var_if_none(java_path)
    (out, err) = run_cmd_get_output([java_path, '-version'])

    #todo: how to apply map on dict.values
    #    regexs = {
    #        "version": _java_version_regex,
    #        "bits": _java_bit_arch_regex,
    #    }

    keys = ["version", "bits"]
    regexs = [_java_version_regex, _java_bit_arch_regex]

    def matcher( regex):
        match = regex.search(err)
        return match.groups()[0] if match else None

    matches = map(matcher, regexs)
    result = dict(zip(keys, matches))

    return result


def _parse_version(s):
    # returns an array of numbers stripping out non numerical chars
    slist = re.findall("\d+", s )
    return [ int(x) for x in slist ]


def check_java_version( check_version, min_required_version ):
    if _parse_version( check_version ) < _parse_version( min_required_version ):
        raise Exception("%s java version is older than required %s" % (check_version,min_required_version) )


def check_java_req( min_version, bits_required=None, java_path=None ):

    java_path = _get_java_path_from_env_var_if_none(java_path)
    java_details = get_java_details(java_path)

    logger.info("java path: %s" % java_path)
    logger.info("java details: %s" % java_details)

    if bits_required and java_details["bits"] is not str(bits_required):
        raise Exception("%s bit java required found '%s'" % (bits_required, java_details["bits"]) )

    check_java_version( java_details["version"], min_version )


def check_visual_studio_installed():
    is_valid = winregutils.is_app_installed(winregutils.VS_2008_REDIST)
    if not is_valid:
        raise Exception("visual studio 2008 redistributable is not installed")
