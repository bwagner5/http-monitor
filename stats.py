from tabulate import tabulate
from datetime import datetime
import pandas
import numpy
import calendar


class Stats(object):
    def __init__(self, alert):
        self.count_dict = dict()
        self.traffic = {'date': [], 'count': []}
        self.traffic_in_interval = 0
        self.alert = int(alert)
        self.alert_messages = []
        self.headers = ["Website", "Count", "Record"]

    def record(self, record):
        section = record.get_section()
        if (section is None):
            return
        self.traffic_in_interval += 1
        entry = self.count_dict.get(section, None)
        if entry is None:
            self.count_dict[section] = (1, record)
        else:
            self.count_dict[section] = (entry[0] + 1, record)
        self.traffic['date'].append(
            calendar.timegm(datetime.timetuple(record.datetime)))
        self.traffic['count'].append(1)
        print(self.traffic)

    def check_alerts(self):
        data = pandas.DataFrame(self.traffic)
        data = data.set_index('date')
        data.index = pandas.to_datetime(data.index, unit='s')
        interval = data.groupby(pandas.TimeGrouper(freq='2Min'))
        avg_interval = data.resample('2Min').sum()
        print(avg_interval)
        # print([
        #     method for method in dir(avg_interval)
        #     if callable(getattr(avg_interval, method))
        # ])
        if avg_interval.count >= self.alert:
            self.alert_messages.append(
                "High traffic generated an alert - hits = %i, triggered at %s"
                % (self.traffic_in_interval, str(datetime.now())))

    def get_alerts_string(self):
        self.traffic_in_interval = 0
        return self.alert_messages

    def number_of_rows(self):
        return len(self.count_dict.keys())

    def __str__(self):
        tabular_data = [[k, v[0], v[1]] for k, v in self.count_dict.items()]
        return tabulate(tabular_data, self.headers, tablefmt="grid")