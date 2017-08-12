"""Responsible for watching a log file and reporting on it"""
from log_parser import LogParser
from pygtail import Pygtail


class LogWatcher(object):

    def __init__(self, stats, log_file):
        self.stats = stats
        self.log_file = log_file

    def run(self):
        parser = LogParser()
        while True:
            for line in Pygtail(self.log_file):
                record = parser.parse(line)
                self.stats.record(record)