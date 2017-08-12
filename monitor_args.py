"""Argument Parsing module for HTTP Monitor"""
from abc import ABCMeta, abstractmethod
from datetime import datetime
import argparse


class MonitorArgsInterface:
    """Interface for argument setup and parsing"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def setup(self):
        """A method called to setup the argument parsing"""
        raise NotImplementedError

    @abstractmethod
    def parse(self):
        """A method called to parse actual arguments"""
        raise NotImplementedError

    @abstractmethod
    def getArgs(self):
        """Retrieves arguments parsed"""
        raise NotImplementedError


class CLIMonitorArgs(MonitorArgsInterface):
    """Command Line Interface implementation for argument parsing"""

    def __init__(self):
        self.parser = None
        self.args = dict()

    def setup(self):
        self.parser = argparse.ArgumentParser(description="HTTP Monitor")

        self.parser.add_argument(
            "-a", 
            "--alert", 
            default=10, 
            help="Alert threshold (default is 10)", 
            type=self.__valid_positive_int
        )
        self.parser.add_argument(
            "-f",
            "--file",
            default="requests_at_same_time.log.txt",
            help="HTTP Access Log to read from (default reads from requests_at_same_time.log.txt)"
        )
        self.parser.add_argument(
            "-w",
            "--window",
            default=120,
            help="Time window in seconds (default is 120 seconds)",
            type=self.__valid_positive_int
        )
        self.parser.add_argument(
            "-t",
            "--test_window_end",
            help="Test window upper bound in UTC for testing (ie. \"2017-08-08 23:03:20\")",
            type=self.__valid_date
        )

    def parse(self):
        self.args = vars(self.parser.parse_args())

    def getArgs(self):
        return self.args

    def __valid_date(self, arg):
        try:
            return datetime.strptime(arg, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(arg)
            raise argparse.ArgumentTypeError(msg)
        
    def __valid_positive_int(self, arg):
        try:
            if int(arg) > 0:
                return int(arg)
            else:
                raise Exception()
        except Exception:
            msg = "Not a valid positive integer: '{0}'.".format(arg)
            raise argparse.ArgumentTypeError(msg)

    def __str__(self):
        return str(self.args)
