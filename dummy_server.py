#!/usr/bin/python3.5
from http.server import HTTPServer, BaseHTTPRequestHandler


class DummyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("data:", post_data)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


def main(host="", port=9991):
    httpd = HTTPServer((host, port), DummyHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
