import sys

from managers.container import Container


def initialize_container() -> Container:
    provider = "minio"  # default will be configured to allow running only one chosen test(without running entire suite)
    if len(sys.argv) > 1:
        provider = sys.argv[1]
    return Container(provider=provider)


def url(docker: Container) -> str:
    return f'http://{docker.container_ip}'
