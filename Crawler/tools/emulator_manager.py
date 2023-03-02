#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time

from bs4 import BeautifulSoup
from ppadb.client import Client as AdbClient

DEBUG_SANDBOX = True

class AdbUtilities():

    def __init__(self, host='127.0.0.1', port=5037):
        self.client = None

        self.host = host
        self.port = port

        # name of the emulator to boot up
        self.emulator_name = "CrawlerGPlay"

        self._connect_to_adb_client()

    def _connect_to_adb_client(self):
        '''
        Connect to adb client, raise exception in case
        some error happen.
        '''
        try:
            self.client = AdbClient(host=self.host, port=self.port)
        except Exception as e:
            print(f"[-] Exception connecting to Adbclient: {str(e)}")
            raise e

    def _start_googleplay_with_package_name(self, pkg_name: str, device_id: str):
        '''
        Start google play through an intent with the package name
        of the application to download.
        '''
        device = self.client.device(device_id)

        print("Running 'am start -a android.intent.action.VIEW -d market://details?id=%s'" % (pkg_name))

        device.shell("am start -a android.intent.action.VIEW -d https://play.google.com/store/apps/details?id=%s" % (pkg_name))

        time.sleep(2)

    def _click_googleplay_on_install(self, device_id: str):
        '''
        Click on the button install in the google play.
        '''
        device = self.client.device(device_id)

        print("Running 'input tap 800 800'")

        device.shell("input tap 800 800")

        time.sleep(2)
    
    def _get_path_to_apk(self, pkg_name: str, device_id: str) -> str:
        '''
        Get the path to the APK file given the package name
        we need to check for the output of an ADB command.
        '''
        device = self.client.device(device_id)

        print("Running 'pm path %s'" % (pkg_name))

        for i in range(30): # up to 5 minutes of waiting
            time.sleep(10)
            print("Retrieving application from package %s" % (pkg_name))
            output = device.shell("pm path %s" % (pkg_name))
            
            if output != '':
                apk = output.split('package:')[1].strip()
                print(f"Retrieved path to apk from {pkg_name}: {apk}")
                return apk
        
        print(f"It wasn't possible to retrieve {pkg_name}")
        return None
    
    def _uninstall_apk(self, pkg_name: str, device_id: str):
        '''
        Uninstall everything from the APK!
        '''
        device = self.client.device(device_id)

        print(f"Uninstalling apk with package name {pkg_name}")

        ret = device.shell("pm uninstall %s" % (pkg_name))

        if "Success" in ret:
            print("Success uninstalling the application!")
        else:
            print("Something weird happened...")

    def _retrieve_apk(self, device_id: str, path_on_device: str, path_on_host: str):
        '''
        Download from the device an apk to the host
        path specified.
        '''    
        device = self.client.device(device_id)

        print(f"Retrieving apk from {path_on_device} to {path_on_host}")

        device.pull(path_on_device, path_on_host)

    def _is_current_focus_googleplay(self, device_id: str):
        '''
        Get what activity is currently on the focus
        on the system, this must be 'com.android.vending'
        in other case, cannot continue downloading...
        '''
        device = self.client.device(device_id)

        print(f"Retrieving current focus application")

        ret = device.shell("dumpsys activity | grep top-activity")

        if not "com.android.vending" in ret:
            print("Current focus is not google play")
            return False
        else:
            print("Current focus is google play!")
            return True

    def get_current_screen_xml(self, device_id: str):
        '''
        Get the XML of the current screen, this can be useful
        to know if there has been some problem downloading the
        apk.
        '''
        device = self.client.device(device_id)

        data = device.shell('uiautomator dump /dev/tty')
        data = data.replace('UI hierchary dumped to: /dev/tty\n','')

        return BeautifulSoup(data,"lxml")

    def is_content_available_in_country(self, data: BeautifulSoup):
        '''
        Check if the text "This item isn't available in your country."
        appears in a Node, in that case, it means content isn't available.
        '''

        ret = data.find("node",{'content-desc':"This item isn't available in your country."})
        
        # if None, it means content is available
        return (ret is None) 

    def is_device_compatible(self, data: BeautifulSoup):
        '''
        Check if current device is compatible
        '''
        ret = data.find("node",{'content-desc':"Your device isn\'t compatible with this version."})

        # if None, it means device is compatible
        return (ret is None)

    def check_cannot_install_apk_press_got_it(self, device_id: str):
        '''
        Check if there's an screen of cannot uninstall, and
        in that case, press the button of "Got it"

        we will press:
        adb shell input tap 882 1757

        This is taken from the bounds, in this way: bounds="[816,1135][948,1245]"
        (816+948)/2 = 882
        (1135+1245)/2 = 1757
        '''
        device = self.client.device(device_id)

        data = self.get_current_screen_xml(device_id)

        ret = data.find("node",{'text':"Try again, and if it still doesn\'t work, see common ways to fix the problem"})

        if ret is not None:
            device.shell("input tap %d %d" % ((816+948)/2, (1135+1245)/2))
            time.sleep(2)

        ret = data.find("node",{'text':"Unrestricted Internet"})
        if ret is not None:
            device.shell("input tap %d %d" % ((816+948)/2, (1107+1217)/2))
            time.sleep(2)

        

    def download_apks_from_emulator(self, pkg:str, path_to_dump_apks: str):
        '''
        From a list of package names, download them from google play
        one by one.
        '''
        # id for the device, in this case as only one is taken
        # I hard code it like emulator-5554
        device_id = "emulator-5554"

        print('Starting google play')
        self._start_googleplay_with_package_name(pkg, device_id)

        if not self._is_current_focus_googleplay(device_id):
            print(f'Error accessing {pkg} in google play')
            return False

        data_from_screen = self.get_current_screen_xml(device_id)

        if not self.is_device_compatible(data_from_screen):
            return False
        
        if not self.is_content_available_in_country(data_from_screen):
            return False

        self.check_cannot_install_apk_press_got_it(device_id)


        print('Click on google play install button')
        self._click_googleplay_on_install(device_id)

        print("Getting the path to the apk")
        apk_path = self._get_path_to_apk(pkg, device_id)

        if apk_path == None or apk_path == '':
            print(f'Error accessing {pkg} in the device')
            return False

        print("Retriving apk to host")
        folder_for_apk = "%s/%s/" % (path_to_dump_apks, pkg)
        if not os.path.exists(folder_for_apk):
            os.mkdir(folder_for_apk)
        self._retrieve_apk(device_id, apk_path, folder_for_apk+"base.apk")

        print("Uninstaling apk")
        self._uninstall_apk(pkg, device_id)

        self.check_cannot_install_apk_press_got_it(device_id)

        return True
        

def main():
    '''
    Just for testing
    '''
    
    list_of_packages = [
        "com.robtopx.geometrydashmeltdown",
        "com.gamedevltd.modernstrike",
        "com.bitsmedia.android.muslimpro",
        "com.julian.fastracing",
        "com.adobe.psmobile",
        "com.hitrock.hideonline",
        "com.olzhas.carparking.multyplayer"
    ]

    adbutils = AdbUtilities()
    adbutils.download_apks_from_emulator(list_of_packages,"apks/")
    

if __name__ == '__main__':
    main()
