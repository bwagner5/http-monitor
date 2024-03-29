"""Data class to represent the a log record"""

from dateutil.parser import parse
from dateutil import tz
from furl import furl


class LogRecord(object):
    def __init__(self, logDict):
        self.remote_host = logDict['h']
        self.request = logDict['r']
        self.user_identifier = logDict['Useragent']
        self.user = logDict['u']
        self.datetime = logDict['time']
        self.timezone = logDict['timezone']
        self.status_code = logDict['s']
        self.size = logDict['b']
        self.section = None
        self.http_verb = None
        self.__post_init()

    def __post_init(self):
        self.__to_utc(self.datetime)
        self.section = self.__parse_section()
        self.http_verb = self.__parse_http_verb()

    def get_http_verb(self):
        return self.http_verb

    def get_section(self):
       return self.section

    def __parse_http_verb(self):
        request_url_list = self.request.split(" ")
        if len(request_url_list) < 2:
            return None
        return request_url_list[0][1:]

    def __parse_section(self):
        request_url_list = self.request.split(" ")
        if len(request_url_list) < 2:
            return None
        url = furl(request_url_list[1])
        path_list = str(url.path).split("/")
        section = path_list[1] if len(path_list) > 1 else ""
        return "%s/%s" % (url.origin, section)

    def __to_utc(self, datetime_obj):
        if self.timezone:
            datetime_str = str(datetime_obj) + " " + str(self.timezone)
            self.datetime = parse(datetime_str).astimezone(tz.tzutc())
            self.timezone = "+0000"

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.remote_host,
                                                   self.request,
                                                   self.user_identifier,
                                                   self.user, 
                                                   self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                                   self.timezone,
                                                   self.status_code, self.size)
