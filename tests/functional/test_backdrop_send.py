from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from io import StringIO
import os
import tempfile
import threading
import unittest
from hamcrest import is_, assert_that
import mock
import backdrop


class HttpStub(BaseHTTPRequestHandler):

    requests = []

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


class TestBackdropSend(unittest.TestCase):

    def setUp(self):
        HttpStub.reset()
        self.httpd = HTTPServer(("", 8000), HttpStub)
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join()

    def test_it_posts_data_to_bucket_url_with_auth_token(self):

        f = tempfile.NamedTemporaryFile(suffix=".json")
        f.write('{"key": "value"}')
        f.flush()

        backdrop.send(["--url", "http://localhost:8000/bucket",
                       "--token", "bucket-auth-token",
                       f.name])

        request = HttpStub.last_request()

        assert_that(request["path"], is_("/bucket"))
        assert_that(request["body"], is_('{"key": "value"}'))
        assert_that(request["headers"]["content-type"], is_("application/json"))
        assert_that(request["headers"]["authorization"], is_("Bearer bucket-auth-token"))

    def test_it_reads_data_from_stdin_to_post_to_backdrop(self):

        data_to_send = StringIO(u'{"key": "value"}')

        backdrop.send(["--url", "http://localhost:8000/bucket",
                       "--token", "bucket-auth-token"], input=data_to_send)

        request = HttpStub.last_request()

        assert_that(request["path"], is_("/bucket"))
        assert_that(request["body"], is_('{"key": "value"}'))
        assert_that(request["headers"]["content-type"], is_("application/json"))
        assert_that(request["headers"]["authorization"], is_("Bearer bucket-auth-token"))

