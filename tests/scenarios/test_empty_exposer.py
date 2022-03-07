import filecmp
import requests

from suite_helpers.s3be_test_case import S3BucketExposerTestCase
from suite_helpers.functions import url


class TestEmptyExposer(S3BucketExposerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.docker.set_exposer_type("empty")
        cls.docker.start_container()

    def test_list_of_buckets(self):
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

    def test_download_existing_binary_object(self):
        r = requests.get(f'{url(self.docker)}/download/cats/cat1.jpg')
        self.assertEqual(r.status_code, 200)
        with open("/tmp/tested_cat.jpg", 'wb') as f:
            f.write(r.content)
        self.assertTrue(  # consistency check
            open("tests/assets/cat1.jpg", "rb").read() == open("/tmp/tested_cat.jpg", "rb").read())

    def test_download_existing_text_object(self):
        r = requests.get(f'{url(self.docker)}/download/cats/nested/nested.txt')
        self.assertEqual(r.status_code, 200)
        with open("/tmp/tested_text.txt", 'w') as f:
            f.write(r.content.decode())
        self.assertTrue(  # consistency check
            filecmp.cmp("tests/assets/nested.txt", "/tmp/tested_text.txt", shallow=False))

    def test_download_not_existing_object(self):
        r = requests.get(f'{url(self.docker)}/download/nope/error.txt')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.text, "")
