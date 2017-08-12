"""implements storage of hits and alarms based off a time window"""
from datetime import datetime, timedelta, timezone, date
from tabulate import tabulate


class Stats(object):
    def __init__(self, alert, window_in_seconds, test_window_end):
        self.count_dict = dict()
        self.alert = int(alert)
        self.window_in_seconds = int(window_in_seconds)
        self.alert_messages = []
        self.is_alerting = False
        self.records = []
        self.headers = ["Website", "Count", "Record"]
        if test_window_end:
            self.test_window_end = test_window_end.replace(tzinfo=timezone.utc)
        else:
            self.test_window_end = None

    def record(self, record):
        section = record.get_section()
        if (section is None):
            return
        entry = self.count_dict.get(section, None)
        if entry is None:
            self.count_dict[section] = (1, record)
        else:
            self.count_dict[section] = (entry[0] + 1, record)
        self.records.append(record)

    def check_alerts(self):
        utc_now = datetime.now(timezone.utc)
        if self.test_window_end:
            window_list = self.__reduce_to_window(self.test_window_end)
            self.test_window_end =  self.test_window_end + timedelta(seconds=2)
        else:
            window_list = self.__reduce_to_window(utc_now)
        count_in_window = len(window_list)
        avg_hits = count_in_window/self.window_in_seconds
        if avg_hits >= self.alert and not self.is_alerting:
            self.alert_messages.append(
                "High traffic generated an alert - hits = %i, triggered at %s"
                % (count_in_window, str(utc_now)))
            self.is_alerting = True
        elif avg_hits < self.alert and self.is_alerting:
            self.is_alerting = False
            self.alert_messages.append(
                "Alert recovered at %s" % (str(utc_now))
            )
        

    def get_alerts_string(self):
        return self.alert_messages

    def number_of_rows(self):
        return len(self.count_dict.keys())

    def __reduce_to_window(self, window_end_datetime):
        window_list = []
        window_start_datetime = window_end_datetime - timedelta(seconds=self.window_in_seconds)
        for record in reversed(self.records):
            if( record.datetime >= window_start_datetime and record.datetime <= window_end_datetime ):
                window_list.append(record)
        return window_list

    def __str__(self):
        tabular_data = [[k, v[0], v[1]] for k, v in self.count_dict.items()]
        return tabulate(tabular_data, self.headers, tablefmt="grid")