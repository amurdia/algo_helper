# ==================================== Meta ==================================== #
'''
Author: Ankit Murdia
Contributors:
Version: 0.0.1
Created: 2020-08-15 12:32:00
Updated: 2020-07-30 10:07:03
Description:
Notes:
To do:
'''
# ============================================================================== #


# ================================ Dependencies ================================ #
import logging
import logging.handlers
import os
from logging.handlers import RotatingFileHandler as RFHandler
# ============================================================================== #


# ================================= Constants ================================== #
logger_map = {}
# ============================================================================== #


# ================================= Code Logic ================================= #
#  Callable methods

#  Abstracted classes
class Logger(object):
    def __init__(self, logger_obj, debug=False):
        self.logger = logger_obj
        self.is_debug = debug

    def debug(self, message):
        if self.is_debug == 'true':
            self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def exception(self, message):
        self.logger.exception(message)


class LogHelper(object):

    """LogHelper class provides a common logging utility.
    
    Attributes:
        formatter (str): Grok used for logging.
        logger (object): Logger object.
        path (str): File path where the logs will be stored.
    """
    
    def __init__(self):
        """Initializer method for LogHelper.
        """
        self.path = '/var/logs/'
        self.formatter = '[%(asctime)s - %(module)s - %(levelname)s - %(process)s] %(message)s'

    def getLogger(self, name, **kwargs):
        """Method to setup a new logger.
        
        Args:
            name (str): Log file name.
            **kwargs: Dynamic kist of keyword arguments.
        
        Returns:
            dict: Map of all the loggers created and in use currently.
        """
        self.path = kwargs.get('path', self.path)
        self.formatter = kwargs.get('formatter', self.formatter)

        if not name in logger_map:
            self.logger = logging.getLogger(name)
            self.logger.setLevel(getattr(logging, 'INFO'))

            fh = RFHandler(os.path.join(os.path.abspath(self.path), name + '.log'), maxBytes=1024 * 1024 * 100, backupCount=10, delay=0.05)
            fh.setLevel(logging.DEBUG)

            # create console handler with a higher log level
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            # create formatter and add it to the handlers
            formatter = logging.Formatter(self.formatter)
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # add the handlers to the logger
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

            logger_map[name] = self.logger

        return logger_map[name]

log = LogHelper()
# ============================================================================== #


# ================================ CLI Handler ================================= #
if __name__ == "__main__":
    pass
# ============================================================================== #