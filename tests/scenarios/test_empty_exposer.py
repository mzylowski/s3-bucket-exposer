import requests
from unittest import TestCase

from test_helpers import initialize_container, url


class TestEmptyExposer(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docker = initialize_container()
        cls.docker.set_exposer_type("empty")
        cls.docker.start_container()

    @classmethod
    def tearDownClass(cls):
        cls.docker.stop_delete_container()

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
