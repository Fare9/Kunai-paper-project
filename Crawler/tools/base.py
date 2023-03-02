#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Base class for each one of the tools
'''

import logging
import configparser
from pathlib import Path


class BaseTool(object):

    NAME = "BaseTool"
    VERSION = "0.1"

    FORMAT = '%(asctime)s [%(levelname)-5.5s] %(message)s'
    config_file = "%s/config.ini" % (Path().absolute())

    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO, format=BaseTool.FORMAT, handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ])
        self.logger = logging.getLogger("Tooling")
        self.logger.info("Creating Tool Object")

        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(BaseTool.config_file)
        self.logger.info("Read Config")

    def config(self) -> None:
        '''
        Whatever the tool needs as configuration, include it here, it will
        be called before run (ALWAYS!)
        '''
        pass

    def run(self, args: dict) -> dict:
        '''
        Whatever the tool has to do, put it in here, do not worry base class
        do nothing, but your tool must return a proper output.
        '''
        return dict()
