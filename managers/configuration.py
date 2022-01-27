import os

from managers import consts


class MissingRequiredConfigurationField(Exception):
    pass


class ValueForConfigFieldNotAllowed(Exception):
    pass


class ConfigurationManager(object):
    _conf = {
        "S3_PROVIDER": {
            "required": True,
            "default:": None,
            "allowed_values": consts.SUPPORTED_S3_PROVIDERS,
            "value": None
        },
        "MINIO_ENDPOINT": {
            "required": False,
            "default:": "http://127.0.0.1:9000",
            "allowed_values": [],
            "value": None
        },
        "S3_ACCESS_KEY": {
            "required": True,
            "default:": None,
            "allowed_values": [],
            "value": None
        },
        "S3_SECRET_KEY": {
            "required": True,
            "default:": None,
            "allowed_values": [],
            "value": None
        },
    }

    @staticmethod
    def _read_env_variable(variable_name):
        value = None
        try:
            value = os.environ[variable_name]
            if ConfigurationManager._conf[variable_name]['allowed_values']:
                if value not in ConfigurationManager._conf[variable_name]['allowed_values']:
                    raise ValueForConfigFieldNotAllowed(
                        f"Value {value} for variable {variable_name}"
                        f" is not allowed. Choose from: f{ConfigurationManager._conf[variable_name]['allowed_values']}")
        except KeyError:
            if ConfigurationManager._conf[variable_name]['required']:
                raise MissingRequiredConfigurationField(
                    f"Variable {variable_name} needs to be configured.")
            if ConfigurationManager._conf[variable_name]['default']:
                value = ConfigurationManager._conf[variable_name]['default']
        return value

    @staticmethod
    def _get_variable(variable):
        if ConfigurationManager._conf[variable]["value"] is None:
            ConfigurationManager._conf[variable]["value"] = ConfigurationManager._read_env_variable(variable)
        return ConfigurationManager._conf[variable]["value"]

    @staticmethod
    def get_s3_provider():
        return ConfigurationManager._get_variable("S3_PROVIDER")

    @staticmethod
    def get_minio_endpoint():
        return ConfigurationManager._get_variable("MINIO_ENDPOINT")

    @staticmethod
    def get_s3_access_key():
        return ConfigurationManager._get_variable("S3_ACCESS_KEY")

    @staticmethod
    def get_s3_secret_key():
        return ConfigurationManager._get_variable("S3_SECRET_KEY")
