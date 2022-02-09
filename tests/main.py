import requests

from managers.container import Container


def sanity_check():
    sanity = Container("minio")
    sanity.start_container()
    r = requests.get(f'http://{sanity.container_ip}')
    assert r.status_code == 200


if __name__ == "__main__":
    sanity_check()
    print("Starting tests scenarios...")
    # TODO
