#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Run a scrapper for Google play to retrieve
information about a specific APK, interesting
information could be the category of the
application.
'''

import random
import time
from tools.base import BaseTool

from google_play_scraper import app
from google_play_scraper import exceptions


class GoogleMetaInf(BaseTool):

    NAME = "GooglePlayInformation"
    VERSION = "0.1"

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("[%s] Started tool" % (GoogleMetaInf.NAME))
        self.seconds_wait = 0

    def config(self) -> None:
        '''
        Configure values for this tool
        '''
        pass

    def run(self, args: dict) -> dict:
        '''
        Run the scrapper for GooglePlay and retrieve the
        metadata, keep only interesting information,
        no interested on comments...
        :param args: {"package_name":<package name of app>}
        :return: metadata from google play
        '''
        self.logger.info("[%s] Running tool" % (GoogleMetaInf.NAME))
        package_name = args["package_name"]
        self.logger.info("[%s] Retrieving information from '%s'" %
                         (GoogleMetaInf.NAME, package_name))
        output_from_scrapper = None
        try:
            output_from_scrapper = app(
                package_name,
                lang="en",
                country="us")
        except exceptions.NotFoundError as nfe:
            return {"EXCEPTION": "Application with package name %s not found on Google Play" % (package_name)}
        except Exception as e:
            return {"EXCEPTION": str(e)}

        if output_from_scrapper is None or len(output_from_scrapper) == 0:
            return {"ERROR": "NOT_ANALYZED",
                    "MESSAGE": "Scrapper could not retrieve information from package name"}

        for k in ["screenshots", "video", "videoImage", "comments", "histogram", "descriptionHTML", "recentChangesHTML"]:
            if k in output_from_scrapper.keys():
                del output_from_scrapper[k]

        return output_from_scrapper
