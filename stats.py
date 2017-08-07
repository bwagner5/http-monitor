class Stats(object):
    def __init__(self):
        self.stats_dict = dict()

    def record(self, record):
        if self.stats_dict.has_key():
            self.stats_dict[record] = self.stats_dict[record] + 1

    def check_alerts(self):
        pass
