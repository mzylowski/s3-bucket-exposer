import filecmp
import requests
from bs4 import BeautifulSoup

from suite_helpers.s3be_test_case import S3BucketExposerTestCase
from suite_helpers.functions import url


class TestHTMLExposer(S3BucketExposerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.docker.set_exposer_type("html")
        cls.docker.start_container()

    def test_list_of_buckets(self):
        expected_buckets = ["cats", "downloads", "secrets"]
        r = requests.get(f'{url(self.docker)}/')
        self.assertEqual(r.status_code, 200)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a', href=True)
        buckets = [link.text.split()[0] for link in links]
        self.assertEqual(expected_buckets, buckets)

    def test_object_list_has_back_link(self):
        r = requests.get(f'{url(self.docker)}/bucket/downloads')
        self.assertEqual(r.status_code, 200)
        soup = BeautifulSoup(r.text, 'html.parser')
        link = soup.find('a', href=True)
        self.assertEqual("<<", link.text)

    def test_list_of_objects_in_existing_bucket(self):
        expected_objects = [
            {
                "name": "cat1.jpg",
                "size": "803.74 KB"
            }, {
                "name": "cat2.jpg",
                "size": "427.40 KB"
            }, {
                "name": "nested/nested.txt",
                "size": "32.00 B"
            }]
        r = requests.get(f'{url(self.docker)}/bucket/cats')
        self.assertEqual(r.status_code, 200)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table')
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            self.assertEqual(cells[0].text, expected_objects[0]["size"])
            self.assertEqual(cells[2].text, expected_objects[0]["name"])
            del expected_objects[0]

    def test_list_of_objects_in_not_existing_bucket(self):
        r = requests.get(f'{url(self.docker)}/bucket/not_exist')
        self.assertEqual(r.status_code, 404)
        self.assertTrue(r.text.__contains__("404 - Object not found"))

    def test_not_existing_endpoint(self):
        r = requests.get(f'{url(self.docker)}/not_exist')
        self.assertEqual(r.status_code, 404)
        self.assertTrue(r.text.__contains__("404 - Object not found"))

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
        self.assertTrue(r.text.__contains__("404 - Object not found"))
