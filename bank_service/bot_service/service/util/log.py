"""the logger module



Typical usage:
from log import logger


logger.info("hello world")
"""
import logging
import os
import sys
import coloredlogs

from queue import Queue
from logging.handlers import QueueHandler, QueueListener


class PackagePathFilter(logging.Filter):
    def filter(self, record):
        pathname = record.pathname
        record.relativepath = None
        abs_sys_paths = map(os.path.abspath, sys.path)
        for path in sorted(abs_sys_paths, key=len, reverse=True):  # longer paths first
            if not path.endswith(os.sep):
                path += os.sep
            if pathname.startswith(path):
                record.relativepath = os.path.relpath(pathname, path)
                break
        return True


logger = logging.getLogger()
logger.setLevel(logging.INFO)

__logQueue = Queue()

logger.addHandler(QueueHandler(__logQueue))
logger.addFilter(PackagePathFilter())

__cformatter = coloredlogs.ColoredFormatter('%(asctime)s  %(relativepath)s:%(lineno)s\t: %(levelname)s %(message)s')
__chandler = logging.StreamHandler()
__chandler.setFormatter(__cformatter)

__formatter = logging.Formatter('%(asctime)s  %(relativepath)s:%(lineno)s\t: %(levelname)s %(message)s')
__fhandler = logging.FileHandler("yoz.log")
__fhandler.setFormatter(__formatter)

__listener = QueueListener(__logQueue, __chandler, __fhandler)
__listener.start()