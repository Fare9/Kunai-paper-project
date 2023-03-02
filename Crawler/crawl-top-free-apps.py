#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Crawl in the Google Play from an Android emulator
for applications to download.
'''

import logging
import pandas as pd
from tools.google_meta_inf import GoogleMetaInf
from tools.emulator_manager import AdbUtilities
from database_connector import DatabaseConnector


FORMAT = '%(asctime)s [%(levelname)-5.5s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, handlers=[
    logging.FileHandler("debug.log"),
    logging.StreamHandler()
])

logger = logging.getLogger()

# https://androidrank.org/android-most-popular-google-play-apps?category=all&sort=4&price=free
TOP_FREE_APPS_CSV = "./applist.csv"
google_meta_inf = GoogleMetaInf()
adbutilities = AdbUtilities()
database_connector = DatabaseConnector()


path_for_apks = "apks/" # path where to download the APK files

def read_apps_information_from_csv() -> pd.DataFrame:
    '''
    Read the CSV with information from the CSV of
    TOP_FREE_APPS, this will be transformed into
    a DataFrame, and from here the information will
    be obtained.
    '''
    global TOP_FREE_APPS_CSV
    global logger

    logger.info("Reading top downloaded apps from [%s]" % (TOP_FREE_APPS_CSV))
    data_top_apps = pd.read_csv(TOP_FREE_APPS_CSV)
    logger.info("Obtained data from 500 top free apps by downloads.")

    return data_top_apps

def obtain_meta_inf_from_pkg_name(pkg_name: str) -> dict:
    '''
    Use the GoogleMetaInf class for obtaining information
    from the applications to analyze.
    '''
    global google_meta_inf
    global logger

    logger.info("Obtaining meta-information from package %s" % (pkg_name))
    information = google_meta_inf.run({"package_name": pkg_name})
    logger.info("Obtained information from package %s" % (pkg_name))
    return information

def obtain_packages_from_googleplay(pkg_names: list):
    '''
    Use the AdbUtilities object to download the list of
    packages from google play, this object will connect
    directly to an emulator since we need to use google
    play from an emulator.
    '''
    global adbutilities

    adbutilities.download_apks_from_emulator(pkg_names, path_for_apks)

def main():
    '''
    Main function of the script
    '''
    global database_connector

    database_connector.config()

    packages_data = read_apps_information_from_csv()

    for i in range(0,500,10):
        print(f"Analyzing from {i} to {i+9}")
        for j in range(0,10):
            index = i+j
            pkg_name = packages_data['pkg_name'][index]

            found = database_connector.retrieve_analysis_apk(pkg_name)
            
            if found is not None:
                continue

            app_name = packages_data['app_name'][index]
            category = packages_data['category'][index]
            downloads = int(packages_data['downloads'][index])
            ratings = int(packages_data['ratings'][index])
            average_rating = float(packages_data['average_rating'][index])
            price = str(packages_data['price'][index])
            growth_30_days = float(packages_data['growth_30_days'][index])
            growth_60_days = float(packages_data['growth_60_days'][index])

            print("Obtaining metadata from google play")
            data_from_google = obtain_meta_inf_from_pkg_name(pkg_name)

            path_where_apk_should_be = "%s/%s/base.apk" % (path_for_apks, pkg_name)

            app_data = {
                    'app_name':app_name,
                    'category':category,
                    'downloads':downloads,
                    'ratings':ratings,
                    'average_rating':average_rating,
                    'price':price,
                    'growth_30_days':growth_30_days,
                    'growth_60_dats':growth_60_days,
                    'google_meta_data':data_from_google,
                    'path_apk':path_where_apk_should_be
                }
            
            print("Download apk from emulator")
            ret = adbutilities.download_apks_from_emulator(pkg_name, path_for_apks)

            if not ret:
                app_data['path_apk'] = None
            
            database_connector.insert_analysis_apk(pkg_name, app_data)

if __name__ == "__main__":
    main()