#!/usr/bin/env python
"""HTTP Monitor implementation to read an access log and alert based on a threshold"""

from monitor_args import CLIMonitorArgs
from log_parser import LogParser
from stats import Stats
from pprint import pprint
from pygtail import Pygtail
import time
from threading import Thread


class HttpMonitor(object):
    def __init__(self, args):
        print(args)
        parser = LogParser()
        self.stats = Stats()
        consoleThread = Thread(target=self.console)
        consoleThread.start()
        while True:
            for line in Pygtail(args['file']):
                record = parser.parse(line)
                self.stats.record(record)
                print("GOT LINE")

    def console(self):
        while True:
            print(self.stats)
            time.sleep(10)


if __name__ == '__main__':
    args = CLIMonitorArgs()
    args.setup()
    args.parse()
    HttpMonitor(args.getArgs())
