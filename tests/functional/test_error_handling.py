import tempfile
import unittest
from hamcrest import *
from tests.functional import command
from tests.functional.http_stub import HttpStub


class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        HttpStub.start()

    def tearDown(self):
        HttpStub.stop()

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


