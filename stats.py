"""implements storage of hits and alarms based off a time window"""
from datetime import datetime, timedelta, timezone, date
from tabulate import tabulate
import humanize


class Stats(object):
    def __init__(self, alert, window_in_seconds, test_window_end):
        self.count_dict = dict()
        self.http_verb_count_dict = dict()
        self.status_count_dict = dict()
        self.alert = int(alert)
        self.total_count = 0
        self.total_bytes = 0
        self.window_in_seconds = int(window_in_seconds)
        self.alert_messages = []
        self.is_alerting = False
        self.records = []
        if test_window_end:
            self.test_window_end = test_window_end.replace(tzinfo=timezone.utc)
        else:
            self.test_window_end = None

    def record(self, record):
        section = record.get_section()
        if (section is None):
            return
        self.total_count += 1
        self.total_bytes += int(record.size)
        self.records.append(record)
        self.__record_section_count(record)
        self.__record_http_verb(record)
        self.__record_status(record)

    def __record_status(self, record):
        status = record.status_code
        entry = self.status_count_dict.get(status, None)
        if entry is None:
            self.status_count_dict[status] = 1
        else:
            self.status_count_dict[status] = entry + 1
        
    def __record_http_verb(self, record):
        verb = record.get_http_verb()
        entry = self.http_verb_count_dict.get(verb, None)
        if entry is None:
            self.http_verb_count_dict[verb] = 1
        else:
            self.http_verb_count_dict[verb] = entry + 1

    def __record_section_count(self, record):
        section = record.get_section()
        entry = self.count_dict.get(section, None)
        if entry is None:
            self.count_dict[section] = 1
        else:
            self.count_dict[section] = entry + 1

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
        if not self.alert_messages:
            return "All clear, no alerts!"
        return "\n".join(self.alert_messages)
            

    def __reduce_to_window(self, window_end_datetime):
        window_list = []
        window_start_datetime = window_end_datetime - timedelta(seconds=self.window_in_seconds)
        for record in reversed(self.records):
            if( record.datetime >= window_start_datetime and record.datetime <= window_end_datetime ):
                window_list.append(record)
        return window_list

    def get_total_count(self):
        return self.total_count

    def get_total_size_human_readable(self):
        return humanize.naturalsize(self.total_bytes, binary=True)

    def get_avg_hit_size(self):
        if self.total_count > 0:
            return humanize.naturalsize(self.total_bytes / self.total_count, binary=True)

    def get_status_tabular_string(self):
        status_count_str = [[k, v] for k, v in self.status_count_dict.items()]
        return tabulate(status_count_str, ["Status Code", "Count"], tablefmt="grid")

    def get_http_verbs_tabular_string(self):
        verb_count_str = [[k, v] for k, v in self.http_verb_count_dict.items()]
        return tabulate(verb_count_str, ["HTTP Verb", "Count"], tablefmt="grid")

    def get_section_count_tabular_string(self):
        section_count_str = [[k, v] for k, v in self.count_dict.items()]
        return tabulate(section_count_str,  ["Website", "Count"], tablefmt="grid")
