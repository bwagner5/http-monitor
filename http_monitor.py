#!/usr/bin/env python
"""HTTP Monitor implementation to read an access log and alert based on a threshold"""

from monitor_args import CLIMonitorArgs
from log_parser import LogParser
from pprint import pprint
from pygtail import Pygtail
import time


class HttpMonitor(object):
    def __init__(self, args):
        print(args)
        parser = LogParser()
        while True:
            for line in Pygtail(args['file']):
                print(parser.parse(line))


if __name__ == '__main__':
    args = CLIMonitorArgs()
    args.setup()
    args.parse()
    HttpMonitor(args.getArgs())
