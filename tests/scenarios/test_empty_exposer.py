import requests

from suite_helpers.s3be_test_case import S3BucketExposerTestCase
from suite_helpers.functions import url

has_failures = []


class TestEmptyExposer(S3BucketExposerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.docker.set_exposer_type("empty")
        cls.docker.start_container()

    def test_list_of_buckets(self):
        self.defaultTestResult()
        r = requests.get(f'{url(self.docker)}/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "")

    def test_list_of_objects_in_existing_bucket(self):
        r = requests.get(f'{url(self.docker)}/bucket/cats')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "")

    def test_list_of_objects_in_not_existing_bucket(self):
        r = requests.get(f'{url(self.docker)}/bucket/not_exist')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "")

    def test_not_existing_endpoint(self):
        r = requests.get(f'{url(self.docker)}/not_exist')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.text, "")

    # TODO (tests for objects download)
