"""Parses Common Log Formatted files into log_record objects"""

from abc import ABCMeta, abstractmethod
from clfparser import CLFParser
from log_record import LogRecord

class ParserInterface:
    """Interface for parsing a log file"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, record):
        """Parse a log file line"""
        raise NotImplementedError


class LogParser(ParserInterface):
    """Implementation of a Parser"""

    def parse(self, record):
        return LogRecord(CLFParser.logDict(record))