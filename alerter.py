"""Responsible for checking for a possible alert"""
import time

class Alerter(object):

    def __init__(self, stats):
        self.stats = stats

    def run(self):
        while True:
          self.stats.check_alerts()
          time.sleep(1)