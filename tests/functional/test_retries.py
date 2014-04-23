import tempfile
import unittest
from hamcrest import *
from tests.functional import command
from tests.functional.http_stub import HttpStub


class TestRetries(unittest.TestCase):
    def setUp(self):
        HttpStub.start()

    def tearDown(self):
        HttpStub.stop()

    def test_it_passes_after_default_number_of_retries(self):
        HttpStub.set_response_codes(500, 500, 200)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/data_set "
                         "--sleep 0 "
                         "--token data_set-auth-token", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_(0))

    def test_it_passes_after_specified_number_of_retries(self):
        HttpStub.set_response_codes(500, 500, 500, 200)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/data_set "
                         "--token data_set-auth-token "
                         "--sleep 0 "
                         "--attempts 4", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_(0))

    def test_it_fails_after_specified_number_of_retries(self):
        HttpStub.set_response_codes(500, 500, 200)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/data_set "
                         "--token data_set-auth-token "
                         "--sleep 0 "
                         "--attempts 2", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_not(0))

