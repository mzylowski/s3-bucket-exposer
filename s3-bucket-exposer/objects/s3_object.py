units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']


class S3Object(object):
    def __init__(self, name, date, size):
        self.name = name
        self.date = date
        self.size = size

    def get_size(self):
        return self._human_size(self.size)

    def _human_size(self, fsize, unit=0):
        return "{:.2f} {}".format(float(fsize), units[unit]) if fsize < 1024 else self._human_size(fsize / 1024,
                                                                                                   unit=unit + 1)

    def get_date(self):
        return self.date.strftime("%Y-%m-%d %H:%M")
