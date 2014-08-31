Bitshares Auto-Feeder
=====================

This is a little python script which automatically updates feed prices for
your delegate

How to use
----------

0. Edit config.json

```javascript
{
    "interval": 7200, // How often should this script update the feed prices? (in seconds)
    "bitshares_rpc": {
        "user": "btsx", // RPC Username
        "pswd": "btsx", // RPC Password
        "host": "127.0.0.1", // Host of bitsharesx daemon
        "port": 1800 // Port of the plain JSONRPC interface
    },
    "wallet": {
        "name": "default", // Name of the wallet your delegate is in
        "unlock_pswd": "" // Password of the wallet
    },
    "delegates": [ // Delegates to update
        "killerbyte"
    ]
}
```

0. Run the script: ```python2 feeder.py```. If all goes well, you should see no errors, and your delegate's feed prices will be updated

0. Turn the feeder into a daemon: ```screen python2 feeder.py```

0. Vote for me!

```
wallet_approve_delegate killerbyte
```

Having Trouble?
---------------
Post your troubles and any related information on the thread for this on http://bitsharestalk.org/
