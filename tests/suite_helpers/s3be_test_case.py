from unittest import TestCase

from suite_helpers.functions import initialize_container


class S3BucketExposerTestCase(TestCase):
    original_failureException = TestCase.failureException

    @property
    def failureException(self):
        self.container_id_for_logs.append(self.docker)
        return self.original_failureException

    def tearDown(self):
        if self.docker.log_contains("Exception"):
            self.fail("Exception occurred during test.")

    @classmethod
    def setUpClass(cls):
        cls.container_id_for_logs = []
        cls.docker = initialize_container()

    @classmethod
    def tearDownClass(cls):
        for container in set(cls.container_id_for_logs):
            print(f">>>>>>>>>>>> Docker logs for {container.container} ({container.container_ip})")
            cls.docker.print_container_logs()
            print("<<<<<<<<<<<<")
        cls.docker.stop_delete_container()
