import tempfile
import unittest
from hamcrest import *
from tests.functional import command
from tests.functional.http_stub import HttpStub


class TestTimeout(unittest.TestCase):
    def setUp(self):
        HttpStub.start()

    def tearDown(self):
        HttpStub.stop()

    def test_it_fails_when_request_takes_longer_than_default_timeout(self):
        HttpStub.set_response_delay(7)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token token "
                         "--failfast", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_not(0))
        assert_that(cmd.stderr, contains_string(
            "Unable to send to backdrop. "
            "Request timeout."))

    def test_it_fails_when_request_takes_longer_than_specified_timeout(self):
        HttpStub.set_response_delay(2)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token token "
                         "--timeout 1 "
                         "--failfast", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_not(0))
        assert_that(cmd.stderr, contains_string(
            "Unable to send to backdrop. "
            "Request timeout."))

    def test_it_passes_when_request_takes_less_than_specified_timeout(self):
        HttpStub.set_response_delay(1)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token token "
                         "--timeout 5 "
                         "--failfast", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_(0))
