import socket
import json
import decimal

def EncodeDecimal(o):
    if isinstance(o, decimal.Decimal):
        return round(o, 8)
    raise TypeError(repr(o) + " is not JSON serializable")

class JSONRPCException(Exception):
    def __init__(self, error):
        self.error = error

class Connection(object):
    id = 1

    def __init__(self, host, port, s = None, method = None):
        self.s = s
        self.method = method
        if not self.s:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, port))


    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            # Python internal stuff
            raise AttributeError
        if self.method:
            name = "{}.{}".format(self.method, name)
        return Connection(None, None, s = self.s, method = name)

    def __call__(self, *args):
        Connection.id += 1
        call = json.dumps({'version': '1.1',
                        'method': self.method,
                        'params': args,
                        'id': Connection.id },
                        default = EncodeDecimal) + '\n'
        self.s.sendall(call)

        res = ''

        # Wait until line is terminated
        while True:
            data = self.s.recv(1024)
            if not data: raise IOError()
            res += data
            if data.rfind('\n'): break
        res = json.loads(res, parse_float = decimal.Decimal)
        if 'error' in res:
            raise JSONRPCException(res['error'])
        elif 'result' not in res:
            raise JSONRPCException({
                'code': -343, 'message': 'missing JSON-RPC result'})
        return res['result']
