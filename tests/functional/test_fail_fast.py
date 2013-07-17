import tempfile
import unittest
from hamcrest import *
from tests.functional import command
from tests.functional.http_stub import HttpStub


class TestFailFast(unittest.TestCase):
    def setUp(self):
        HttpStub.start()

    def tearDown(self):
        HttpStub.stop()

    def test_it_fails_fast_when_flag_is_set(self):
        HttpStub.set_response_codes(500, 200)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token token "
                         "--failfast", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_(8))

    def test_it_fails_fast_when_set_and_also_passed_attempts(self):
        HttpStub.set_response_codes(500, 200, 200, 200, 200)
        cmd = command.do("./backdrop-send "
                         "--url http://localhost:8000/bucket "
                         "--token token "
                         "--failfast "
                         "--attempts 5 ", stdin='{"key": "value"}')

        assert_that(cmd.exit_status, is_(8))

