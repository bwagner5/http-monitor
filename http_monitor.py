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
from log_watcher import LogWatcher
from alerter import Alerter
from console import Console
from stats import Stats


class HttpMonitor(object):
    
    def __init__(self, args):
        self.args = args
        self.stats = Stats(args['alert'], args['window'], args['test_window_end'])
        self.console = Console(self.stats, self.args)
        self.log_watcher = LogWatcher(self.stats, self.args['file'])
        self.alerter = Alerter(self.stats)
        threads = self.__setup_threads()
        self.__start_threads(threads)
        self.__keep_alive()

    def __setup_threads(self):
        consoleThread = Thread(target=self.console.run)
        logWatchThread = Thread(target=self.log_watcher.run)
        alertingThread = Thread(target=self.alerter.run)
        return [consoleThread, alertingThread, logWatchThread]

    def __start_threads(self, threads):
        for thread in threads:
            thread.daemon = True
            thread.start()

    def __keep_alive(self):
        while True:
            time.sleep(.5)


def signal_handler(args, signal, frame):
    os.remove(args.getArgs()['file'] + ".offset")
    #curses.endwin() ## This will reset terminal settings, but clears window as well
    sys.exit(0)


if __name__ == '__main__':
    args = CLIMonitorArgs()
    args.setup()
    args.parse()
    signal.signal(signal.SIGINT, partial(signal_handler, args))
    HttpMonitor(args.getArgs())
