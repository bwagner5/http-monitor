from tabulate import tabulate

class Stats(object):

    def __init__(self):
        self.count_dict = dict()
        self.headers = ["Website", "Count"]

    def record(self, record):
        section = record.get_section()
        self.count_dict[section] = self.count_dict.get(section, 0) + 1

    def check_alerts(self):
        pass

    def __str__(self):
        tabular_data = [[k,v] for k, v in self.count_dict.items()]
        return tabulate(tabular_data, self.headers, tablefmt="grid")