import tempfile
import unittest
from hamcrest import *
from tests.functional import command
from tests.functional.http_stub import HttpStub


class TestCoreFunctionality(unittest.TestCase):
    def setUp(self):
        HttpStub.start()

    def tearDown(self):
        HttpStub.stop()

    def test_it_posts_data_to_data_set_url_with_auth_token(self):
        f = tempfile.NamedTemporaryFile(suffix=".json")
        f.write('{"key": "value"}')
        f.flush()

        command.do("./backdrop-send "
                   "--url http://localhost:8000/data_set "
                   "--token data_set-auth-token %s" % f.name)

        request = HttpStub.last_request()

        assert_that(request["path"], is_("/data_set"))
        assert_that(request["body"], is_('{"key": "value"}'))
        assert_that(request["headers"]["content-type"],
                    is_("application/json"))
        assert_that(request["headers"]["authorization"],
                    is_("Bearer data_set-auth-token"))

    def test_it_reads_data_from_stdin_to_post_to_backdrop(self):
        command.do("./backdrop-send "
                   "--url http://localhost:8000/data_set "
                   "--token data_set-auth-token", stdin='{"key": "value"}')

        request = HttpStub.last_request()

        assert_that(request["path"], is_("/data_set"))
        assert_that(request["body"], is_('{"key": "value"}'))
        assert_that(request["headers"]["content-type"],
                    is_("application/json"))
        assert_that(request["headers"]["authorization"],
                    is_("Bearer data_set-auth-token"))

