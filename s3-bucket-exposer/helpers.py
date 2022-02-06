import logging

from configuration import consts
from configuration.config import Configuration
from providers import minio, aws
from exposers import html, json, base


def initialize():
    configure_logging()
    provider = spawn_provider()
    connectivity_check(provider)
    return provider, spawn_exposer()


def connectivity_check(provider):
    logging.info("[INIT TEST] Performing connectivity check by getting list of buckets...")
    try:
        if Configuration.get_exposer_allowed_buckets() == consts.ALL_BUCKETS_ALLOWED:
            logging.warning("! All buckets accessible by provided credentials will be exposed. Use this with caution. "
                            "Please note that any bucket added in the future also will be exposed. It is recommended "
                            "to configure allowed buckets by EXPOSER_ALLOWED_BUCKETS variable.")
        buckets = provider.list_of_buckets()
        logging.debug(f"[INIT TEST] Detected buckets are: {','.join(buckets)}")
    except Exception as e:
        logging.critical("[INIT TEST] Middleware (boto3) thrown exception during connecting to s3")
        raise e
    else:
        logging.info("[INIT TEST] Connectivity check passed! :)")


def configure_logging():
    log_level = Configuration.get_log_level()
    if log_level is not consts.NO_EXPOSER_LOGGING:
        logging.getLogger().setLevel(log_level)


def spawn_provider():
    provider = Configuration.get_s3_provider()
    if provider == consts.MINIO_PROVIDER:
        return minio.MinioProvider()
    elif provider == consts.AWS_PROVIDER:
        return aws.AWSProvider()
    else:
        raise Exception(f"Unsupported S3 provider: {provider}")


def spawn_exposer():
    exposer = Configuration.get_exposer_type()
    if exposer not in consts.SUPPORTED_EXPOSER_TYPES:
        raise Exception(f"Unsupported Exposer type: {exposer}")
    if exposer == consts.HTML_EXPOSER:
        return html.HTMLExposer()
    elif exposer == consts.JSON_EXPOSER:
        return json.JSONExposer()
    else:
        return base.BaseExposer()
