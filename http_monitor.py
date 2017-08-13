#!/usr/bin/env python
"""HTTP Monitor implementation to read an access log and alert based on a threshold"""

import os
import sys
import time
import curses
from threading import Thread
from datetime import datetime
import signal
from functools import partial
from monitor_args import CLIMonitorArgs
from log_watcher import LogWatcher
from alerter import Alerter
from console import Console
from stats import Stats
from subprocess import call


class HttpMonitor(object):
    
    def __init__(self, args):
        self.args = args
        self.__check_for_testing()
        self.stats = Stats(args['alert'], args['window'], args['test_window_end'])
        self.console = Console(self.stats, self.args)
        self.log_watcher = LogWatcher(self.stats, self.args['file'])
        self.alerter = Alerter(self.stats)
        threads = self.__setup_threads()
        self.__start_threads(threads)
        self.__keep_alive()

    def __setup_threads(self):
        consoleThread = Thread(target=self.console.run, name="console")
        logWatchThread = Thread(target=self.log_watcher.run, name="logWatcher")
        alertingThread = Thread(target=self.alerter.run, name="alerter")
        return [consoleThread, alertingThread, logWatchThread]

    def __start_threads(self, threads):
        for thread in threads:
            if self.args['test3'] and thread.name == "console":
                continue
            thread.daemon = True
            thread.start()

    def __keep_alive(self):
        while True:
            time.sleep(.5)

    def __check_for_testing(self):
        if self.args['test1']:
            self.__test_1()
        if self.args['test2']:
            self.__test_2()
        if self.args['test3']:
            self.__test_3()

    def __test_1(self):
        print("Executing Test 1")
        self.args['test_window_end'] = datetime(2017, 8, 8, 23, 3, 20)
        self.args['file'] = 'requests_at_same_time.log.txt'

    def __test_2(self):
        print("Executing Test 2")
        fake_logs_thread = Thread(target=self.__fake_logs)
        fake_logs_thread.daemon = True
        fake_logs_thread.start()
        time.sleep(3)
        self.args['file'] = "access.log"

    def __fake_logs(self):
        call(["python", "Fake-Apache-Log-Generator/apache-fake-log-gen.py", "-n", "0", "-o", "LOG"])

    def __test_3(self):
        print("Executing Test 3")
        self.args['test_window_end'] = datetime(2017, 8, 8, 23, 3, 20)
        self.args['file'] = 'requests_at_same_time.log.txt'
        test_3_thread = Thread(target=self.__test_3_thread)
        test_3_thread.daemon = True
        test_3_thread.start()

    def __test_3_thread(self):
        time.sleep(2)
        timeout = time.time() + 60*1   # 1 minute from now
        alerted = False
        while True:
            if self.stats.is_alerting:
                alerted = True
            if alerted and not self.stats.is_alerting:
                print("TEST PASSED!")
                sys.exit(0)
            if time.time() > timeout:
                print("TEST FAILED!")
                sys.exit(1)
            time.sleep(1)
        




def signal_handler(args, signal, frame):
    try:
        os.remove(args.getArgs()['file'] + ".offset")
    except:
        pass
    #curses.endwin() ## This will reset terminal settings, but clears window as well
    sys.exit(0)


if __name__ == '__main__':
    args = CLIMonitorArgs()
    args.setup()
    args.parse()
    signal.signal(signal.SIGINT, partial(signal_handler, args))
    HttpMonitor(args.getArgs())
