from unittest import TestCase, mock

from objects.s3_object import S3Object
from configuration.consts import APP_VERSION
from exposers.html import HTMLExposer


class TestHTMLExposer(TestCase):
    def setUp(self):
        self.foo = HTMLExposer()

    @mock.patch('exposers.html.render_template')
    def test_expose_list_of_buckets(self, mocked_fun):
        self.foo.expose_list_of_buckets(["foo", "bar"])
        mocked_fun.assert_called_with('bucket_list.html',
                                      buckets=['foo', 'bar'],
                                      product_version=f's3-bucket-exposer {APP_VERSION}')

    @mock.patch('exposers.html.render_template')
    def test_expose_list_of_objects(self, mocked_fun):
        s3_object = S3Object("foo", "0", "1024")
        self.foo.expose_list_of_objects("bar", [s3_object])
        mocked_fun.assert_called_with('object_list.html',
                                      bucket='bar',
                                      objects=[s3_object],
                                      product_version=f's3-bucket-exposer {APP_VERSION}')

    @mock.patch('exposers.html.abort')
    def test_expose_list_of_objects_None(self, mocked_fun):
        self.foo.expose_list_of_objects("bar", None)
        mocked_fun.assert_called_with(404)
