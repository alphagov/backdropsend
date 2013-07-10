from io import StringIO
import unittest
import mock
import backdrop


class TestBackdropSend(unittest.TestCase):

    @mock.patch('requests.post')
    def test_it_posts_data_to_bucket_url_with_auth_token(self, post):
        input = StringIO(u'{"key": "value"}')
        backdrop.send(["http://backdrop-bucket-url", "bucket-auth-token"], input)

        post.assert_called_with(
            url="http://backdrop-bucket-url",
            data=u'{"key": "value"}',
            headers={
                'Authorization': 'Bearer bucket-auth-token',
                'Content-type': 'application/json'
            },
        )
