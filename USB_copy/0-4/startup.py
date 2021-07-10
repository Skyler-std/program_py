# -*- coding: utf-8 -*-


from psutil import Popen
from tkinter import messagebox, Tk


try:
    with open('C:/Easy USB Backup Info.pyc') as i:
        fileContent = i.readlines()
    fileContent = fileContent[0]
    Popen('start ' + fileContent, shell=True)
except FileNotFoundError:
    root = Tk()
    root.withdraw()
    if (messagebox.showerror("Error", "File C:\Easy USB Backup Info.pyc is wrong!!!")) == 'ok':
        root.destroy()
