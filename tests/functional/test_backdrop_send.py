import tempfile
import unittest
from hamcrest import *
from tests.functional import command
from tests.functional.http_stub import HttpStub


class TestBackdropSend(unittest.TestCase):
    def setUp(self):
        HttpStub.start()

    def tearDown(self):
        HttpStub.stop()

    def test_it_posts_data_to_bucket_url_with_auth_token(self):
        f = tempfile.NamedTemporaryFile(suffix=".json")
        f.write('{"key": "value"}')
        f.flush()

        command.do("./backdrop-send "
                   "--url http://localhost:8000/bucket "
                   "--token bucket-auth-token %s" % f.name)

        request = HttpStub.last_request()

        assert_that(request["path"], is_("/bucket"))
        assert_that(request["body"], is_('{"key": "value"}'))
        assert_that(request["headers"]["content-type"],
                    is_("application/json"))
        assert_that(request["headers"]["authorization"],
                    is_("Bearer bucket-auth-token"))

    def test_it_reads_data_from_stdin_to_post_to_backdrop(self):
        command.do("./backdrop-send "
                   "--url http://localhost:8000/bucket "
                   "--token bucket-auth-token", stdin='{"key": "value"}')

        request = HttpStub.last_request()

        assert_that(request["path"], is_("/bucket"))
        assert_that(request["body"], is_('{"key": "value"}'))
        assert_that(request["headers"]["content-type"],
                    is_("application/json"))
        assert_that(request["headers"]["authorization"],
                    is_("Bearer bucket-auth-token"))

    def test_it_fails_if_neither_file_nor_stdin_provided(self):
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token bucket-auth-token")

        assert_that(cmd.exit_status, is_not(0))

    def test_it_reports_http_errors(self):
        HttpStub.set_response_codes(500)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token bucket-auth-token", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_not(0))
        assert_that(cmd.stderr, contains_string("Unable to send to backdrop"))
        assert_that(cmd.stderr, contains_string("500"))

    def test_it_passes_after_default_number_of_retries(self):
        HttpStub.set_response_codes(500, 500, 200)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token bucket-auth-token", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_(0))

    def test_it_reports_connection_errors(self):
        cmd = command.do("./backdrop-send "
                         "--url http://non-existent-url "
                         "--token bucket-auth-token", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_not(0))
        assert_that(cmd.stderr, contains_string("Unable to send to backdrop"))

    def test_it_reports_authorization_errors(self):
        HttpStub.set_response_codes(403)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token wrong-token", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_not(0))
        assert_that(cmd.stderr, contains_string(
            "Unable to send to backdrop. "
            "Unauthorised: check your access token."))

    def test_it_fails_when_request_takes_longer_than_default_timeout(self):
        HttpStub.set_response_delay(7)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token token", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_not(0))
        assert_that(cmd.stderr, contains_string(
            "Unable to send to backdrop. "
            "Connection error."))

    def test_it_fails_when_request_takes_longer_than_specified_timeout(self):
        HttpStub.set_response_delay(2)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token token "
                         "--timeout 1", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_not(0))
        assert_that(cmd.stderr, contains_string(
            "Unable to send to backdrop. "
            "Connection error."))       

    def test_it_passes_when_request_takes_less_than_specified_timeout(self):
        HttpStub.set_response_delay(1)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token token "
                         "--timeout 5", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_(0))            