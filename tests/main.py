import requests
import unittest

from managers.container import Container


def sanity_check():
    sanity = Container("minio")
    sanity.start_container()
    r = requests.get(f'http://{sanity.container_ip}')
    assert r.status_code == 200


if __name__ == "__main__":
    print("Starting tests scenarios...")
    loader = unittest.TestLoader()
    tests = loader.discover('scenarios')
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(tests)
    print(":)") if result.wasSuccessful() else print(":(")
