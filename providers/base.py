class BaseProvider(object):
    def __init__(self):
        self.client = self.get_client()

    def get_client(self):
        pass

    def list_of_buckets(self):
        response = self.client.list_buckets()
        return [b["Name"] for b in response.get("Buckets", [])]
