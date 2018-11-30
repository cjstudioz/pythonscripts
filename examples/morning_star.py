import requests
import logging

BASE_FEED_URL = 'https://mp.morningstarcommodity.com/lds/providers/LIM/datasources/'
METADATA_TEMPLATE = 'https://mp.morningstarcommodity.com/lds/feeds/%s/md'

def _getFeeds(datasourceName):
    datasourceUrl = BASE_FEED_URL + datasourceName
    logging.info('getting: %s' % datasourceUrl)
    print 'getting: %s' % datasourceUrl
    try:
        feedsReq = requests.get(datasourceUrl, auth=auth)   
        feedsJson = feedsReq.json()
        feeds = [feed['name'] for feed in feedsJson['feeds']]
        return feeds
    except RuntimeError as e:
        return e
    
def _getMetadata(feedName):
    feedURL = METADATA_TEMPLATE % feedName
    logging.info('getting: %s' % feedURL)
    try:
        req = requests.get(feedURL, auth=auth)   
        feedJson = req.json()
        return feedJson
    except Exception as e:
        return e
        
auth = ('teodora.baeva@btgpactual.com','S7xL5dtZ')

datasourcesReq = requests.get("https://mp.morningstarcommodity.com/lds/providers/LIM/datasources/", auth=auth)   
datasources = datasourcesReq.json()

feeds = {datasource['name']: _getFeeds(datasource['name']) for datasource in datasources}

metadata = {feed['name']: _getMetadata(feed['name']) for feed in feeds['feeds']}

#OTHER STUFf
datasourcesReq = requests.get('https://mp.morningstarcommodity.com/lds/providers/LIM/datasources/EEX', auth=auth)   
datasources = datasourcesReq.json()

https://mp.morningstarcommodity.com/lds/providers/LIM/datasources/Gfi
https://mp.morningstarcommodity.com/lds/providers/LIM/datasources/%s

url = 'https://mp.morningstarcommodity.com/lds/providers/LIM/datasources/Gfi'
feedsReq = requests.get(url, auth=auth)   
feedsJson = feedsReq.json()

metadataURL = 'https://mp.morningstarcommodity.com/lds/feeds/Eex_GasFuturesPrices/md'
r = requests.get(metadataURL,
    auth=
)