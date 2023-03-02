#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Connect to the MongoDB database and allow
inserting data, retrieve data, and other
kind of operations.
'''

import pymongo
import logging
import configparser
from pathlib import Path


class DatabaseConnector(object):

    NAME = "DatabaseConnector"
    VERSION = "0.1"

    FORMAT = '%(asctime)s [%(levelname)-5.5s] %(message)s'
    config_file = "%s/config.ini" % (Path().absolute())

    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO, format=DatabaseConnector.FORMAT, handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ])

        self.logger = logging.getLogger("Database")
        self.logger.info("Created a DatabaseConnector object")

        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(DatabaseConnector.config_file)

        self.connector = None
        self.database = None
        self.collection = None

    def config(self, uri = None, database = None, collection = None, malware_collection = None) -> None:
        '''
        Configuration of the database as well as the connection
        to the specific collection.
        '''
        if uri is None:
            uri = self.config_parser["DATABASE"]["URI"]
        if database is None:
            database = self.config_parser["DATABASE"]["DATABASE"]
        if collection is None:
            collection = self.config_parser["DATABASE"]["COLLECTION"]
        if malware_collection is None:
            malware_collection = self.config_parser["DATABASE"]["MALWARE_COLLECTION"]

        self.logger.info("[%s] Connecting to URI: %s" %
                         (DatabaseConnector.NAME, uri))

        self.connector = pymongo.MongoClient(uri,
                                             username=self.config_parser["MONGO"]["MONGO_USER"],
                                             password=self.config_parser["MONGO"]["MONGO_PASSWORD"])

        self.logger.info("[%s] Connecting to database 'Analysis'" %
                         (DatabaseConnector.NAME))
        self.database = self.connector[database]

        self.logger.info("[%s] Connecting to collection 'APK'" %
                         (DatabaseConnector.NAME))
        self.collection = self.database[collection]

        self.logger.info("[%s] Connecting to collection 'MALWARE'" % (DatabaseConnector.NAME))
        self.malware_collection = self.database[malware_collection]

    def insert_analysis_apk(self, pkg_name: str, analysis_results: dict) -> None:
        '''
        Insert an analysis result in the database,
        it can be that the hash already exists, so
        we just update the current register of the
        collection.

        :param pkg_name: hash of the APK, used as key of the collection.
        :param analysis_results: results of the analysis.
        '''
        result = self.collection.find_one({"package": pkg_name})
        if result is None:
            self.collection.insert_one(
                {"package": pkg_name, "analysis": analysis_results})
        else:
            filter = {"package": pkg_name}
            newvalues = {"$set": {"analysis": analysis_results}}
            self.collection.update_one(filter=filter, update=newvalues)

    def insert_malware_analysis_apk(self, md5: str, malware_family: str, analysis_results: dict) -> None:
        '''
        Insert a malware analysis in the malware
        collection.

        :param md5: hash of the apk, used as key.
        :param malware_family: malware family from the sample.
        '''
        result = self.malware_collection.find_one({"md5": md5})
        if result is None:
            self.malware_collection.insert_one(
                {"md5": md5, "malware_family": malware_family, "analysis": analysis_results})
        else:
            filter = {"md5": md5}
            newvalues = {"$set": {"analysis": analysis_results}}
            self.malware_collection.update_one(filter=filter, update=newvalues)

    def retrieve_analysis_apk(self, pkg_name: str) -> dict:
        '''
        Retrieve an analysis by its hash,
        in case the analysis does not exist, 
        the method just returns None.

        :param pkg_name: hash to look for in the collection.
        :return: dictionary with the result of the analysis or None.
        '''
        return self.collection.find_one({"package": pkg_name})

    def retrieve_malware_analysis_apk(self, md5: str) -> dict:
        '''
        Retrieve an analysis from the malware collection.

        :param md5: hash from the sample
        :return: dictionary with the results
        '''
        return self.malware_collection.find_one({"md5", md5})

    def retrieve_all_the_documents_from_collection(self) -> pymongo.cursor.Cursor:
        '''
        Retrieve all the documents from the specified
        collection in config.ini.

        :return: Cursor with all the documents from the collection.
        '''
        return self.collection.find({})

    def retrieve_all_documents_from_malware_collection(self) -> pymongo.cursor.Cursor:
        '''
        Retrieve all the documents from the malware collection.
        '''
        return self.malware_collection.find({})

    def execute_a_find_query(self, query: dict) -> pymongo.cursor.Cursor:
        '''
        Run a find query into database, the query
        will be specified this time by the user.

        :param query: what to find in the database.
        :return: Cursor of values that match the query.
        '''
        return self.collection.find(query)

    def execute_a_find_query_malware(self, query: dict) -> pymongo.cursor.Cursor:
        '''
        Run a find query into database, the query
        will be specified this time by the user.

        :param query: what to find in the database.
        :return: Cursor of values that match the query.
        '''
        return self.malware_collection.find(query)

    def get_number_of_values_by_query(self, query: dict) -> int:
        '''
        Get the number of values that match a query.

        :param query: what to find in the database.
        :return: integer with the number of documents that match the query.
        '''
        return self.collection.count_documents(query)

    def get_number_of_values_by_query_malware(self, query: dict) -> int:
        '''
        Get the number of values that match a query.

        :param query: what to find in the database.
        :return: integer with the number of documents that match the query.
        '''
        return self.malware_collection.count_documents(query)