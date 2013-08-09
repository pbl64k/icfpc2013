
from secret import secret

import httplib
import json

class Client:
    def __init__(self):
        pass

    def invoke(self, name, param):
        rq_body = json.dumps(param)
        cn = httplib.HTTPConnection('icfpc2013.cloudapp.net')
        cn.request('POST', '/' + name + '?auth=' + secret, rq_body)
        resp = cn.getresponse()
        data = json.loads(resp.read())
        return resp.status, resp.reason, data

