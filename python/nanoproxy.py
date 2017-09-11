import SocketServer
import SimpleHTTPServer
import urllib


LISTEN_PORT = 9999
PROXY_BASEURL = "http://127.0.0.1:8888"


class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.copyfile(urllib.urlopen(PROXY_BASEURL + self.path), self.wfile)

SocketServer.ForkingTCPServer(('', LISTEN_PORT), Proxy).serve_forever()
