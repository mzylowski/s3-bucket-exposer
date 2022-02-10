from unittest import TestCase, mock

from exposers.html import BaseExposer


class TestBaseExposer(TestCase):
    def setUp(self):
        self.foo = BaseExposer()

    def test_expose_list_of_buckets(self):
        return_value = self.foo.expose_list_of_buckets(["foo", "bar"])
        self.assertEqual(return_value, "")

    def test_expose_list_of_objects(self):
        return_value = self.foo.expose_list_of_objects("foo-bucket", ["foo", "bar"])
        self.assertEqual(return_value, "")

    @mock.patch('exposers.base.flask_redirect')
    def test_redirect(self, mocked_fun):
        url = "http://foo"
        self.foo.redirect(url)
        mocked_fun.assert_called_with(url)
