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