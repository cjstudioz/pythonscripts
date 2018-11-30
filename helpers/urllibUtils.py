import os
from tempfile import gettempdir
from urllib2 import urlopen, build_opener, ProxyHandler, install_opener, HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm 
import urllib
import lib.logger as logger

proxy = r"http://leecaf:<paassword>@fm-eu-lon-bc-proxy-rr.fm.rbsgrp.net:8080"

def setupProxy():
    proxy_support = ProxyHandler({"http":proxy, "ftp":proxy})
    opener = build_opener(proxy_support)
    install_opener(opener)
    
def downloadfile(url, dir=None):
    f = urlopen(url)
    print "downloading " + url

    # Open our local file for writing
    dir = dir or gettempdir() 
    localFileName = dir + "/" + os.path.basename(url)
    with open( localFileName, "wb") as local_file:
        local_file.write(f.read())
        
    return localFileName        
    
    
def callWebAPI( url, username='admin', password='HPCT3am', getpost='get', params={} ):
    '''
    convenience function that allows one to specify GEt vs POST and insert authentication
    '''
    
    # determin get post
    data=None
    encodedParams = urllib.urlencode(params)
    
    if params:
        if getpost.lower() == 'get':
            url = r'%s?%s' % ( url, encodedParams )                 
        elif getpost.lower() == 'post': 
            data = encodedParams
        else:
            raise RuntimeError( 'getpost arg should be "get" or "post" found invalid %s' % getpost )
    
    #log
    logger.info( r'calling "%s" wtih params %s' % ( url, encodedParams ) )
    
    #Authentication
    passman = HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    authhandler = HTTPBasicAuthHandler(passman)
    opener = build_opener(authhandler)
    install_opener(opener)
    
    pagehandle = urlopen(url, data=data)
    res = pagehandle.read()
    
    return res    