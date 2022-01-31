import logging

from managers import consts
from managers.configuration import ConfigurationManager as Cm
from providers import minio, aws
from exposers import html, json, base


def initialize():
    configure_logging()
    return spawn_provider(), spawn_exposer()


def configure_logging():
    logging.getLogger().setLevel(Cm.get_log_level())


def spawn_provider():
    provider = Cm.get_s3_provider()
    if provider == consts.MINIO_PROVIDER:
        return minio.MinioProvider()
    elif provider == consts.AWS_PROVIDER:
        return aws.AWSProvider
    else:
        raise Exception(f"Unsupported S3 provider: {provider}")


def spawn_exposer():
    exposer = Cm.get_exposer_type()
    if exposer not in consts.SUPPORTED_EXPOSER_TYPES:
        raise Exception(f"Unsupported Exposer type: {exposer}")
    if exposer == consts.HTML_EXPOSER:
        return html.HTMLExposer()
    elif exposer == consts.JSON_EXPOSER:
        return json.JSONExposer()
    else:
        return base.BaseExposer()
