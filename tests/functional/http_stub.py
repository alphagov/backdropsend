from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading


class HttpStub(BaseHTTPRequestHandler):

    requests = []
    server = None
    thread = None

    @classmethod
    def last_request(cls):
        return cls.requests[0]

    @classmethod
    def reset(cls):
        cls.requests = []

    def do_POST(self):
        self.requests.append( {
            "headers": dict(self.headers),
            "path": self.path,
            "body": self.body()
        })

        self.send_response(200)

        return

    def body(self):
        return self.rfile.read(int(self.headers.getheader('content-length')))

    @classmethod
    def start(cls):
        cls.reset()
        cls.server = HTTPServer(("", 8000), cls)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()

    @classmethod
    def stop(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
