import shutil
import psutil
import threading
import time
import os
import multiprocessing
import urllib
import posixpath
import platform
import subprocess
import asyncio
import importlib
import cmd

# take the note for pid of this thread
with open("pid_protect.txt", mode = "w") as pid_Protect:
    pid_Protect.write(str(os.getpid()))



# start main
def main_start():
    with open("main_start.bat", mode = "w") as main_start:
        main_start.write("@ECHO OFF\n")
        main_start.write("cd ..\n")
        main_start.write("start main0.2.exe\n")
        main_start.write("exit")

    os.system("start main_start.bat")

# check if main is running
while True:
    # get the pid of main
    with open("pid_main.txt") as main_pid:
        Main_pid = main_pid.readlines()[0]

    if int(Main_pid) not in psutil.pids():
        os.system("taskkill /f /im main0.2.exe")
        main_start()
        with open("pid_main.txt", mode = "w") as a:
            pass
        time.sleep(3)
