import json
import requests

from os import listdir, path
from time import sleep
from jsonrpc import Connection, JSONRPCException

def loadFile(p):
    js = open(p)
    data = json.load(js)
    js.close()
    return data

def updateFeeds(config, feeds):
    # Connect to the wallet
    c = Connection(config['bitshares_rpc']['host'], config['bitshares_rpc']['port'])
    try:
        # Login
        c.login(config['bitshares_rpc']['user'], config['bitshares_rpc']['pswd'])
        # Unlock wallet
        c.wallet_open(config['wallet']['name'])
        c.wallet_unlock(60, config['wallet']['unlock_pswd'])
    except JSONRPCException as e:
        print 'Could not connect to bitshares daemon: {}, {}'.format(e.error['code'], e.error['message'])
        return
    except Exception as e:
        print 'Could not connect to bitshares daemon: {}'.format(e)
        return
    print 'Connected!'
    for feed in feeds:
        r = requests.get(feed['url'])
        if r.status_code is 200:
            p = None
            if feed['key']:
                p = r.json()[feed['key']]
            else:
                p = r.text
            print '{}: {}'.format(feed['symbol'], p)
            for delegate in config['delegates']:
                try:
                    c.wallet_publish_price_feed(delegate, p, feed['symbol'])
                except JSONRPCException as e:
                    print 'Could not update price feeds for currency {}, delegate {}: {}: {}'.format(feed['symbol'], delegate, e.error['code'], e.error['message'])
                    #return
    try:
        c.wallet_lock()
    except JSONRPCException as e:
        print 'Could not lock wallet: {}'.format(e.error['message'])

config = loadFile('config.json')

FEEDS_DIR = 'feeds'

feeds = []

# Load the other coin configuration files
for f in listdir(FEEDS_DIR):
    p = path.join(FEEDS_DIR, f)
    if path.isfile(p):
        feeds.append(loadFile(p))

while True:
    print 'Updating feeds...'
    updateFeeds(config, feeds)
    sleep(config['interval'])
