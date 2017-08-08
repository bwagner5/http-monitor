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

    def get_section(self):
        request_url_list = self.request.split(" ")
        if len(request_url_list) < 2:
            return None
        url = furl(request_url_list[1])
        return "%s/%s" % (url.origin, str(url.path).split("/")[1])

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.remote_host,
                                                   self.request,
                                                   self.user_identifier,
                                                   self.user, self.datetime,
                                                   self.timezone,
                                                   self.status_code, self.size)
