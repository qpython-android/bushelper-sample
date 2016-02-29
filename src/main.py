#-*-coding:utf-8-*-  
#qpy:webapp:公交路线查询
#qpy:fullscreen
#qpy://127.0.0.1:8081/
"""
公交路线查询

@Author river
"""

from bottle import Bottle, ServerAdapter
from bottle import static_file, template, request

import urllib2
import os,os.path
#### 常量定义 #########
ASSETS = "/assets/"
ROOT = os.path.dirname(os.path.abspath(__file__))

API_URL = 'http://openapi.aibang.com/bus/lines?app_key=d706b1f36e6adfdb862f7f54c132390f&alt=json'
API_URL2 = 'http://openapi.aibang.com/bus/transfer?app_key=d706b1f36e6adfdb862f7f54c132390f&alt=json'



##################### SL4A ##############
try:
    IS_SL4A = True
    #import androidhelper
    #Droid = androidhelper.Android()
    #Droid.startLocating()
except:
    IS_SL4A = False
    pass


######### QPYTHON WEB SERVER ###############

class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        #sys.stderr.close()
        import threading 
        threading.Thread(target=self.server.shutdown).start() 
        #self.server.shutdown()
        self.server.server_close() 
        print "# QWEBAPPEND"


######### BUILT-IN ROUTERS ###############
def __exit():
    global server
    server.stop()

def __ping():
    return "ok"

def server_static(filepath):
    return static_file(filepath, root=ROOT+'/assets')

def home():
    #if IS_SL4A:
    #    location = Droid.getLastKnownLocation().result
    #    location = location.get('network', location.get('gps'))
    return template(ROOT+'/index.html', city='北京')

def detail():
    city = request.GET['city']
    q = request.GET['keyword']

    data = _get_json_content(API_URL+"&city="+city+"&q="+q)

    return template(ROOT+'/detail.html', data=data)

def transfer():
    city = request.GET['city']
    here = request.GET['here']
    ther = request.GET['ther']

    data = _get_json_content(API_URL2+"&city="+city+"&start_addr="+here+"&end_addr="+ther)
    print data
    return template(ROOT+'/transfer.html',data=data)

def _get_json_content(jurl):
    print jurl
    data = urllib2.urlopen(jurl)
    content = data.read()
    data.close()
    
    return content




######### WEBAPP ROUTERS ###############
app = Bottle()
app.route('/', method='GET')(home)
app.route('/detail', method='GET')(detail)
app.route('/transfer', method='GET')(transfer)
app.route('/__exit', method=['GET','HEAD'])(__exit)
app.route('/__ping', method=['GET','HEAD'])(__ping)
app.route('/assets/<filepath:path>', method='GET')(server_static)

try:
    server = MyWSGIRefServer(host="127.0.0.1", port="8081")
    app.run(server=server,reloader=False)
except Exception,ex:
    print "Exception: %s" % repr(ex)


