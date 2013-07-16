from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading
import time
import errno

class HttpStub(BaseHTTPRequestHandler):

    requests = []
    server = None
    thread = None
    response_code = 200
    response_delay = 0

    @classmethod
    def last_request(cls):
        return cls.requests[0]

    @classmethod
    def reset(cls):
        cls.requests = []
        cls.response_code = 200
        cls.response_delay = 0

    def do_POST(self):
        self.requests.append({
            "headers": dict(self.headers),
            "path": self.path,
            "body": self.body()
        })

        if (self.response_delay > 0):
            time.sleep(self.response_delay)
        
        try:
            self.send_response(self.response_code)
        except IOError, e:
            if e.errno == errno.EPIPE:
                pass
            else:
                raise e

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

    @classmethod
    def set_response_code(cls, code):
        cls.response_code = code

    @classmethod
    def set_response_delay(cls, delay):
        cls.response_delay = delay
