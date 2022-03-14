import requests

from suite_helpers.s3be_test_case import S3BucketExposerTestCase
from suite_helpers.functions import url


class TestRestrictedBuckets(S3BucketExposerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.docker.set_exposer_allowed_buckets(["cats"])
        cls.docker.start_container()

    def test_download_existing_text_object(self):
        r = requests.get(f'{url(self.docker)}/download/cats/nested/nested.txt')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.content.decode() != "")

    def test_download_restricted_text_object(self):
        r = requests.get(f'{url(self.docker)}/download/secrets/secret.txt')
        self.assertEqual(r.status_code, 404)
        self.assertTrue(r.text.__contains__("404 - Object not found"))


class TestAllBucketsAllowed(S3BucketExposerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.docker.start_container()

    def test_warning_in_logs_for_all_buckets_exposed(self):
        self.assertTrue(
            self.docker.log_contains("! All buckets accessible by provided credentials will be exposed. Use this with"))

    def test_download_secret_text_object(self):
        r = requests.get(f'{url(self.docker)}/download/secrets/secret.txt')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.text.__contains__("It's a secret"))
