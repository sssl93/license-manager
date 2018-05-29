import os
import logging.handlers
import logging


class LoggerHandler(object):
    """
    init app logger through the class
    eg. LoggerHandler(log_file_path).log_init()
    """

    def __init__(self, file_path, log_level=None, log=None):
        self.file_path = file_path
        self.log_path = os.path.dirname(file_path)
        self.filename = os.path.basename(file_path)
        self.log_level = self.get_log_level(log_level)
        self.log = log or logging.getLogger(__file__)

    def init_log_dir(self):
        path = self.log_path.strip().rstrip("\\")
        is_exists = os.path.exists(path)
        if not is_exists:
            try:
                os.makedirs(path)
            except Exception:
                return False
        return True

    @staticmethod
    def get_log_level(level):
        return {'debug': logging.DEBUG, 'info': logging.INFO, 'warn': logging.WARN, 'error': logging.ERROR,
                'fatal': logging.FATAL}.get(level, logging.INFO)

    @staticmethod
    def set_log_format(handler):
        fmt = logging.Formatter('%(asctime)s[%(levelname)s] [%(filename)s] LINE:%(lineno)s :%(message)s')
        handler.setFormatter(fmt)

    @staticmethod
    def syslog_handler():
        for log_address in ('/dev/log', '/var/run/syslog'):
            if os.path.exists(log_address):
                return logging.handlers.SysLogHandler(address=log_address)
        return logging.handlers.SysLogHandler()

    def log_init(self):
        if self.init_log_dir():
            log_file = os.path.join(self.log_path, self.filename)
            try:
                handler = logging.FileHandler(log_file, mode='a')
            except Exception:
                handler = self.syslog_handler()
        else:
            handler = self.syslog_handler()
        self.set_log_format(handler)
        self.log.handlers = [handler, logging.StreamHandler()]
        self.log.setLevel(self.log_level)
        return self.log
