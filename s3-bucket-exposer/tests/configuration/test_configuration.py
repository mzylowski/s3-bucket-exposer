import os
from unittest import TestCase, mock

from configuration.config import Configuration, ValueForConfigFieldNotAllowed, MissingRequiredConfigurationField, \
    ConfigFieldNotExist


class TestConfiguration(TestCase):
    def setUp(self):
        for arg in Configuration._conf:
            Configuration._conf[arg]["value"] = None

    @mock.patch.dict(os.environ, {"S3_PROVIDER": "minio"}, clear=True)
    def test_s3_provider_minio_possible(self):
        self.assertEqual(Configuration.get_s3_provider(), "minio")

    @mock.patch.dict(os.environ, {"S3_PROVIDER": "aws"}, clear=True)
    def test_s3_provider_aws_possible(self):
        self.assertEqual(Configuration.get_s3_provider(), "aws")

    @mock.patch.dict(os.environ, {"S3_PROVIDER": "foo"}, clear=True)
    def test_s3_provider_wrong_value(self):
        with self.assertRaises(ValueForConfigFieldNotAllowed):
            Configuration.get_s3_provider()

    def test_s3_provider_required(self):
        with self.assertRaises(MissingRequiredConfigurationField):
            Configuration.get_s3_provider()

    def test_s3_provider_ensure_cannot_change(self):
        with mock.patch.dict(os.environ, {"S3_PROVIDER": "aws"}, clear=True):
            self.assertEqual(Configuration.get_s3_provider(), "aws")
        with mock.patch.dict(os.environ, {"S3_PROVIDER": "minio"}, clear=True):
            self.assertEqual(Configuration.get_s3_provider(), "aws")

    @mock.patch.dict(os.environ, {"MINIO_ENDPOINT": "http://foo.bar"}, clear=True)
    def test_minio_endpoint_positive(self):
        self.assertEqual(Configuration.get_minio_endpoint(), "http://foo.bar")

    def test_minio_endpoint_default(self):
        self.assertEqual(Configuration.get_minio_endpoint(), "http://127.0.0.1:9000")

    @mock.patch.dict(os.environ, {"S3_ACCESS_KEY": "admin"}, clear=True)
    def test_s3_access_key_positive(self):
        self.assertEqual(Configuration.get_s3_access_key(), "admin")

    def test_s3_access_key_required(self):
        with self.assertRaises(MissingRequiredConfigurationField):
            Configuration.get_s3_access_key()

    @mock.patch.dict(os.environ, {"S3_SECRET_KEY": "password"}, clear=True)
    def test_s3_secret_key_positive(self):
        self.assertEqual(Configuration.get_s3_secret_key(), "password")

    def test_s3_secret_key_required(self):
        with self.assertRaises(MissingRequiredConfigurationField):
            Configuration.get_s3_secret_key()

    @mock.patch.dict(os.environ, {"EXPOSER_ALLOWED_BUCKETS": "foo, bar,download"}, clear=True)
    def test_exposer_allowed_buckets_positive(self):
        self.assertEqual(Configuration.get_exposer_allowed_buckets(), ["foo", "bar", "download"])

    def test_exposer_allowed_buckets_all(self):
        self.assertEqual(Configuration.get_exposer_allowed_buckets(), "all_buckets")

    @mock.patch.dict(os.environ, {"EXPOSER_ALLOWED_BUCKETS": "foo_as ad sasd ag  ,  ads a bar,"}, clear=True)
    def test_exposer_allowed_buckets_spaces_remover(self):
        self.assertEqual(Configuration.get_exposer_allowed_buckets(), ['foo_asadsasdag', 'adsabar'])

    @mock.patch.dict(os.environ, {"EXPOSER_ALLOWED_BUCKETS": ""}, clear=True)
    def test_exposer_allowed_buckets_empty(self):
        self.assertEqual(Configuration.get_exposer_allowed_buckets(), [])

    def test_exposer_type_default(self):
        self.assertEqual(Configuration.get_exposer_type(), "html")

    @mock.patch.dict(os.environ, {"EXPOSER_TYPE": "html"}, clear=True)
    def test_exposer_type_html(self):
        self.assertEqual(Configuration.get_exposer_type(), "html")

    @mock.patch.dict(os.environ, {"EXPOSER_TYPE": "json"}, clear=True)
    def test_exposer_type_json(self):
        self.assertEqual(Configuration.get_exposer_type(), "json")

    @mock.patch.dict(os.environ, {"EXPOSER_TYPE": "empty"}, clear=True)
    def test_exposer_type_empty(self):
        self.assertEqual(Configuration.get_exposer_type(), "empty")

    @mock.patch.dict(os.environ, {"EXPOSER_TYPE": "foo"}, clear=True)
    def test_exposer_type_wrong_value(self):
        with self.assertRaises(ValueForConfigFieldNotAllowed):
            Configuration.get_exposer_type()

    @mock.patch.dict(os.environ, {"EXPOSER_LOG_LEVEL": "FOO"}, clear=True)
    def test_exposer_log_level_wrong_value(self):
        with self.assertRaises(ValueForConfigFieldNotAllowed):
            Configuration.get_log_level()

    @mock.patch.dict(os.environ, {"EXPOSER_LOG_LEVEL": "CRITICAL"}, clear=True)
    def test_exposer_log_level_positive(self):
        self.assertEqual(Configuration.get_log_level(), "CRITICAL")

    def test_exposer_log_level_default(self):
        self.assertEqual(Configuration.get_log_level(), "ERROR")

    def test_print_variable_non_restricted_exposer_type(self):
        self.assertEqual(Configuration.print_variable("EXPOSER_TYPE"), "html")

    @mock.patch.dict(os.environ, {"S3_SECRET_KEY": "password"}, clear=True)
    def test_print_variable_restricted(self):
        self.assertEqual(Configuration.print_variable("S3_SECRET_KEY"), "********")

    def test_print_variable_that_not_exist(self):
        with self.assertRaises(ConfigFieldNotExist):
            Configuration.print_variable("foo")
