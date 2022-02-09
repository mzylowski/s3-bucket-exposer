import docker
import time

from managers import consts


class Container(object):
    def __init__(self, provider):
        self.client = docker.APIClient(base_url='unix://var/run/docker.sock')
        self.container = None
        self.container_ip = None

        self._minio_endpoint = None
        self._set_s3_provider(provider)
        self._s3_access_key = consts.S3_ACCESS_KEY_DEFAULT
        self._s3_secret_key = consts.S3_SECRET_KEY_DEFAULT
        self._exposer_allowed_buckets = None
        self._exposer_type = None
        self._exposer_log_level = consts.EXPOSER_LOG_LEVEL_DEFAULT

    def __del__(self):
        self.stop_delete_container()

    def start_container(self):
        container = self.client.create_container(f"{consts.DOCKER_IMAGE_NAME}:{consts.DOCKER_IMAGE_TAG}",
                                                 detach=True,
                                                 ports=[80],
                                                 environment=self._build_env_dict(),
                                                 host_config=self.client.create_host_config(
                                                     port_bindings={80: 80})
                                                 )

        self.container = container['Id']
        self.client.start(self.container)
        inspect = self.client.inspect_container(self.container)
        self.container_ip = inspect['NetworkSettings']['Networks']['bridge']['IPAddress']
        print(f"Container started with IP {self.container_ip} (id: {self.container})")
        time.sleep(2)  # (todo: remove sanity check from main.py and do while with timeout checking for exit code 200

    def stop_delete_container(self):
        if self.container:
            self.client.stop(self.container)
            self.client.remove_container(self.container)
            self.container = None

    def _build_env_dict(self):
        envs = {
            consts.S3_PROVIDER: self._s3_provider,
            consts.S3_ACCESS_KEY: self._s3_access_key,
            consts.S3_SECRET_KEY: self._s3_secret_key,
            consts.EXPOSER_LOG_LEVEL: self._exposer_log_level,
        }
        if self._s3_provider == "minio":
            envs[consts.MINIO_ENDPOINT] = self._minio_endpoint

        if self._exposer_allowed_buckets:
            envs[consts.EXPOSER_ALLOWED_BUCKETS] = ",".join(self._exposer_allowed_buckets)
        if self._exposer_type:
            envs[consts.EXPOSER_TYPE] = self._exposer_type
        return envs

    def _set_s3_provider(self, provider: str):
        if provider == "minio":
            self._calculate_minio_url()
            self._s3_provider = provider
        elif provider == "aws":
            raise NotImplementedError
        else:
            raise Exception("Not expected provider in tests")

    def _calculate_minio_url(self):
        inspect = self.client.inspect_container(consts.MINIO_CONTAINER_NAME)
        ip = inspect['NetworkSettings']['Networks']['bridge']['IPAddress']
        self._minio_endpoint = f"http://{ip}:9000"

    def set_exposer_allowed_buckets(self, value: []):
        self._exposer_allowed_buckets = value

    def set_exposer_type(self, value: str):
        self._exposer_type = value

    def set_log_level(self, value: str):
        self._exposer_log_level = value
