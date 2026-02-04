import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from common.config import Config

config = Config().config

LOG_FILE = ""
LOG_FORMAT = '%(asctime)s %(levelname)s : %(message)s'
LOG_LEVEL = config["log"]["level"]
DATE_TIME = '%d-%m-%Y  %H:%M:%S '

match LOG_LEVEL:
   case "notset":
      LOG_LEVEL = logging.NOTSET
   
   case "debug":
      LOG_LEVEL = logging.DEBUG
   
   case "info":
      LOG_LEVEL = logging.INFO
   
   case "warning":
      LOG_LEVEL = logging.WARNING
   
   case "error":
      LOG_LEVEL = logging.ERROR
   
   case "critical":
      LOG_LEVEL = logging.CRITICAL
   
   case _ :
      LOG_LEVEL = logging.INFO

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_TIME)
   console_handler.setFormatter(formatter)
   return console_handler
def get_file_handler(LOG_FILE):
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_TIME)
   file_handler.setFormatter(formatter)
   return file_handler
def get_logger(service):
   LOG_PATH = config['log']['path']

   # Check if directory exist
   if not os.path.exists(LOG_PATH):
      os.mkdir(LOG_PATH)
   
   # create log file
   LOG_FILE = os.path.join(
                LOG_PATH,
                f'{service}.log'
              )
   logger = logging.getLogger(service)
   logger.setLevel(LOG_LEVEL) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler(LOG_FILE))
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger

    