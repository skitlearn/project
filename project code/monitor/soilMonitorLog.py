# -*- coding: utf-8 -*-
'''
use dbscan algorithm to segment img of soil;
'''
import logging

class SMLog(object):
    logger =  logging.getLogger("SoilMonitor")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        consoleHandle = logging.StreamHandler()
        consoleHandle.setLevel(logging.INFO)
        ch_formatter = logging.Formatter('%(levelname)s - %(message)s')
        consoleHandle.setFormatter(ch_formatter)
        logger.addHandler(consoleHandle)

        fileHandle =logging.FileHandler('soilMonitor.log')
        fileHandle.setLevel(logging.DEBUG)
        fileHandle_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandle.setFormatter(fileHandle_formatter)
        logger.addHandler(fileHandle)


    @staticmethod
    def debug(msg, *args, **kwargs):
        SMLog.logger.debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg, *args, **kwargs):
        SMLog.logger.info(msg, *args, **kwargs)

    @staticmethod
    def warning(msg, *args, **kwargs):
        SMLog.logger.warning(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        SMLog.logger.error(msg, *args, **kwargs)


if __name__ == '__main__':
    num = 0
    SMLog.debug("debug:%s",num)
    SMLog.info(num)
    SMLog.error("error")


