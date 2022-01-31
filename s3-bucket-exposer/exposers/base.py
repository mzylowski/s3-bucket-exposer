from flask import redirect as flask_redirect


class BaseExposer(object):
    def expose_list_of_buckets(self, buckets):
        return ""

    def expose_list_of_objects(self, objects):
        return ""

    def redirect(self, url):
        return flask_redirect(url)
