import shlex
import subprocess
import tempfile
import unittest
from hamcrest import is_, assert_that
from tests.functional.http_stub import HttpStub


class TestBackdropSend(unittest.TestCase):

    def setUp(self):
        HttpStub.start()

    def tearDown(self):
        HttpStub.stop()

    def do_command(self, command, stdin=None):
        p = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE)
        if stdin:
            p.stdin.write(stdin)
        p.communicate()

    def test_it_posts_data_to_bucket_url_with_auth_token(self):

        f = tempfile.NamedTemporaryFile(suffix=".json")
        f.write('{"key": "value"}')
        f.flush()

        self.do_command("bin/backdrop-send "
                        "--url http://localhost:8000/bucket "
                        "--token bucket-auth-token %s" % f.name)

        request = HttpStub.last_request()

        assert_that(request["path"], is_("/bucket"))
        assert_that(request["body"], is_('{"key": "value"}'))
        assert_that(request["headers"]["content-type"], is_("application/json"))
        assert_that(request["headers"]["authorization"], is_("Bearer bucket-auth-token"))

    def test_it_reads_data_from_stdin_to_post_to_backdrop(self):

        self.do_command("bin/backdrop-send "
                        "--url http://localhost:8000/bucket "
                        "--token bucket-auth-token", stdin='{"key": "value"}')

        request = HttpStub.last_request()

        assert_that(request["path"], is_("/bucket"))
        assert_that(request["body"], is_('{"key": "value"}'))
        assert_that(request["headers"]["content-type"], is_("application/json"))
        assert_that(request["headers"]["authorization"], is_("Bearer bucket-auth-token"))
