#!/usr/bin/env python
"""HTTP Monitor implementation to read an access log and alert based on a threshold"""

import os
import sys
import time
import curses
from threading import Thread
import signal
from functools import partial
from monitor_args import CLIMonitorArgs
from log_parser import LogParser
from stats import Stats
from pygtail import Pygtail


class HttpMonitor(object):
    def __init__(self, args):
        self.args = args
        self.stats = Stats(args['alert'])
        consoleThread = Thread(target=self.console)
        logWatchThread = Thread(target=self.log_watch)
        consoleThread.daemon = True
        logWatchThread.daemon = True
        consoleThread.start()
        logWatchThread.start()
        while True:
            time.sleep(.5)

    def log_watch(self):
        parser = LogParser()
        while True:
            for line in Pygtail(self.args['file']):
                record = parser.parse(line)
                self.stats.record(record)

    def alerting(self):
        while True:
            self.stats.check_alerts()
            time.sleep(1)

    def console(self):
        while True:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.stats.check_alerts()
            num_of_rows = (self.stats.number_of_rows() + 1) * 2
            stdscr.addstr(0, 0, "args: " + str(self.args))
            stdscr.addstr(1, 0, str(self.stats))
            stdscr.addstr(num_of_rows + 3, 0,
                          str(self.stats.get_alerts_string()))
            time.sleep(2)


def signal_handler(args, signal, frame):
    os.remove(args.getArgs()['file'] + ".offset")
    sys.exit(0)


if __name__ == '__main__':
    args = CLIMonitorArgs()
    args.setup()
    args.parse()
    signal.signal(signal.SIGINT, partial(signal_handler, args))
    HttpMonitor(args.getArgs())
