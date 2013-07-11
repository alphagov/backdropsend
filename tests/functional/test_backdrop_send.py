from io import StringIO
import os
import tempfile
import unittest
import mock
import backdrop


class TestBackdropSend(unittest.TestCase):

    @mock.patch('requests.post')
    def test_it_posts_data_to_bucket_url_with_auth_token(self, post):

        f = tempfile.NamedTemporaryFile(suffix=".json")
        f.write('{"key": "value"}')
        f.flush()

        backdrop.send(["--url", "http://backdrop-bucket-url",
                       "--token", "bucket-auth-token",
                       f.name])

        self.assert_data_got_sent(post)

    @mock.patch('requests.post')
    def test_it_reads_data_from_stdin_to_post_to_backdrop(self, post):

        data_to_send = StringIO(u'{"key": "value"}')

        backdrop.send(["--url", "http://backdrop-bucket-url",
                       "--token", "bucket-auth-token"], input=data_to_send)

        self.assert_data_got_sent(post)

    def assert_data_got_sent(self, post):
        post.assert_called_with(
            url="http://backdrop-bucket-url",
            data=u'{"key": "value"}',
            headers={
                'Authorization': 'Bearer bucket-auth-token',
                'Content-type': 'application/json'
            },
        )
