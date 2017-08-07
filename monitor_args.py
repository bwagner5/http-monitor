"""Argument Parsing module for HTTP Monitor"""
from abc import ABCMeta, abstractmethod
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
            "-a", "--alert", default=100, help="Alert threshold")
        self.parser.add_argument(
            "-f",
            "--file",
            default="small_example.log.txt",
            help="HTTP Access Log to read from")

    def parse(self):
        self.args = vars(self.parser.parse_args())

    def getArgs(self):
        return self.args

    def __str__(self):
        return str(self.args)
