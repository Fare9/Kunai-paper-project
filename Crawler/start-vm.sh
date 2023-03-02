#!/bin/bash

emulator_path=`which emulator`
if [ -z "$emulator_path" ];
then
    echo "The binary emulator must be accessible."
    echo "Exiting."
    exit
fi

emulator_name=""

get_boot_is_finished(){
        while [ "`adb -s $emulator_name shell getprop sys.boot_completed 2> /dev/null | tr -d '\r' `" != "1" ] ; do sleep 1; done

        result=$(adb -s $emulator_name shell getprop init.svc.bootanim 2> /dev/null)

        if [ "$result" == "stopped" ]; then
                return 1
        fi
                return 0
}

echo "[!] Booting gplay emulator"
emulator -avd CrawlerGPlay -memory 4096 -partition-size 2048 -prop dalvik.vm.heapsize=512m -no-snapshot-load -wipe-data > /dev/null 2> /dev/null &


sleep 2

emulator_name=`adb devices | tail -n 2 | head -n1 | cut -f1 -d$'\t'`

echo "[+] Name of the emulator to check: $emulator_name"

get_boot_is_finished
func_result=$?

while [ $func_result -eq 0 ]
do
    get_boot_is_finished
    func_result=$?
done

sleep 3

echo "[+] Boot has finished"

echo "[!] Finished execution"
echo "$emulator_name"
