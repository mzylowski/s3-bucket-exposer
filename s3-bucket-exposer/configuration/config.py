import logging
import os

from configuration import consts


class MissingRequiredConfigurationField(Exception):
    pass


class ValueForConfigFieldNotAllowed(Exception):
    pass


class ConfigFieldNotExist(Exception):
    pass


class Configuration(object):
    _conf = {
        consts.S3_PROVIDER: {
            "restricted": False,
            "required": True,
            "default": None,
            "allowed_values": consts.SUPPORTED_S3_PROVIDERS,
            "value": None
        },
        consts.MINIO_ENDPOINT: {
            "restricted": False,
            "required": False,
            "default": "http://127.0.0.1:9000",
            "allowed_values": consts.ALL_VALUES_ALLOWED,
            "value": None
        },
        consts.S3_ACCESS_KEY: {
            "restricted": True,
            "required": True,
            "default": None,
            "allowed_values": consts.ALL_VALUES_ALLOWED,
            "value": None
        },
        consts.S3_SECRET_KEY: {
            "restricted": True,
            "required": True,
            "default": None,
            "allowed_values": consts.ALL_VALUES_ALLOWED,
            "value": None
        },
        consts.EXPOSER_ALLOWED_BUCKETS: {
            "restricted": False,
            "required": False,
            "default": consts.ALL_BUCKETS_ALLOWED,
            "allowed_values": consts.ALL_VALUES_ALLOWED,
            "value": None
        },
        consts.EXPOSER_TYPE: {
            "restricted": False,
            "required": False,
            "default": "html",
            "allowed_values": consts.SUPPORTED_EXPOSER_TYPES,
            "value": None
        },
        consts.EXPOSER_LOG_LEVEL: {
            "restricted": False,
            "required": False,
            "default": "ERROR",
            "allowed_values": consts.LOG_LEVELS,
            "value": None
        }
    }

    @staticmethod
    def _read_env_variable(variable_name):
        value = None
        try:
            value = os.environ[variable_name]
            if Configuration._conf[variable_name]['allowed_values']:
                if value not in Configuration._conf[variable_name]['allowed_values']:
                    logging.error(f"Value {value} is not valid for field {variable_name}. Exiting...")
                    raise ValueForConfigFieldNotAllowed(
                        f"Value {value} for variable {variable_name}"
                        f" is not allowed. Choose from: {Configuration._conf[variable_name]['allowed_values']}")
        except KeyError:
            if Configuration._conf[variable_name]['required']:
                logging.critical(f"Missing required variable {variable_name}. Exiting...")
                raise MissingRequiredConfigurationField(
                    f"Variable {variable_name} needs to be configured.")
            if Configuration._conf[variable_name]['default']:
                logging.info(f"Setting {variable_name} variable to default "
                             f"value: {Configuration._conf[variable_name]['default']}")
                value = Configuration._conf[variable_name]['default']
        return value

    @staticmethod
    def _get_variable(variable):
        try:
            if Configuration._conf[variable]["value"] is None:
                Configuration._conf[variable]["value"] = Configuration._read_env_variable(variable)
                logging.debug(f"Variable {variable} configured with value: {Configuration.print_variable(variable)}")
            return Configuration._conf[variable]["value"]
        except KeyError:
            raise ConfigFieldNotExist(f"Variable {variable} is not defined in config.py. This is probably a bug caused"
                                      f"by calling not existing variable from other place in the code.")

    @staticmethod
    def print_variable(variable_name):
        value = Configuration._get_variable(variable_name)
        if Configuration._conf[variable_name]['restricted']:
            return consts.SECRET
        return value

    @staticmethod
    def get_s3_provider():
        return Configuration._get_variable(consts.S3_PROVIDER)

    @staticmethod
    def get_minio_endpoint():
        return Configuration._get_variable(consts.MINIO_ENDPOINT)

    @staticmethod
    def get_s3_access_key():
        return Configuration._get_variable(consts.S3_ACCESS_KEY)

    @staticmethod
    def get_s3_secret_key():
        return Configuration._get_variable(consts.S3_SECRET_KEY)

    @staticmethod
    def get_exposer_allowed_buckets():
        value = Configuration._get_variable(consts.EXPOSER_ALLOWED_BUCKETS)
        if isinstance(value, list):
            return value
        if value == consts.ALL_BUCKETS_ALLOWED:
            return value
        allowed_buckets = list(filter(None, value.replace(" ", "").split(",")))
        logging.info(f"Configured allowed buckets are: {','.join(allowed_buckets)}")
        Configuration._conf["EXPOSER_ALLOWED_BUCKETS"]["value"] = allowed_buckets
        return Configuration._conf["EXPOSER_ALLOWED_BUCKETS"]["value"]

    @staticmethod
    def get_exposer_type():
        return Configuration._get_variable(consts.EXPOSER_TYPE)

    @staticmethod
    def get_log_level():
        return Configuration._get_variable(consts.EXPOSER_LOG_LEVEL)
