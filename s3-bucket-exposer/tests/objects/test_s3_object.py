from datetime import datetime
from unittest import TestCase, mock

from objects import s3_object


class TestS3Object(TestCase):
    def setUp(self):
        self.objFoo = s3_object.S3Object("foo", datetime(2020, 12, 12, 15, 0, 0), 54354687)
        self.objBar = s3_object.S3Object("bar", datetime(2021, 7, 16, 15, 0, 0), 1024)

    @mock.patch.object(s3_object.S3Object, '_human_size')
    def test_get_size(self, mocked_method):
        self.objFoo.get_size()
        mocked_method.assert_called_with(54354687)

    def test__human_size(self):
        self.assertEqual(self.objFoo.get_size(), "51.84 MB")
        self.assertEqual(self.objBar.get_size(), "1.00 KB")

    def test_get_date(self):
        self.assertEqual(self.objFoo.get_date(), "2020-12-12 15:00")
        self.assertEqual(self.objBar.get_date(), "2021-07-16 15:00")
