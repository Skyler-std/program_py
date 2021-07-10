# -*- coding: utf-8 -*-
# coding: unicode_escape


from tkinter import messagebox, Tk, Label, Checkbutton, Entry, Button, Menu
from tkinter import Toplevel, PhotoImage, Canvas, Scrollbar, GROOVE
from tkinter import Frame, Text, filedialog, END
from tkinter import StringVar
from time import strftime, sleep
from psutil import Popen, disk_partitions
from shutil import copytree
from threading import Thread
import webbrowser as web
import os, sys, pygame
import pynput
from json import dump, load


# script path
winPath = os.path.dirname(os.path.realpath(sys.executable))
winPath += '\\'
winpath = list(winPath)
ii = -1
for i in winpath:
    ii += 1
    if i == '\\':
        winpath[ii] = '/'
del i
del ii
path = ''.join(winpath)
del winpath

# Log
def Log(content):
    with open(path + 'Easy USB Backup.log', mode='a+') as log:
        log.write('[' + strftime('%Y') + '/' + strftime('%m') + '/' + strftime('%d') + '  ' + strftime('%H') + ':' + strftime('%M') + ':' + strftime('%S') + ']\n')
        log.write(content + "\n")

Log("Start to check files")
# Lost check
checkL = []
checkNl = ['a.ico', 'b.gif', 'c.png', 'd.pyc', 'e.pyc', 'f.png','Backup.pyc',
           'g.gif', 'h.pyc']

def checkAdd(comment, Comment):
    checkNl.append(str(os.path.exists(path + 'material/' + comment)) + Comment)

checkAdd('a.ico', '0')
checkAdd('b.gif', '1')
checkAdd('c.png', '2')
checkAdd('d.pyc', '3')
checkAdd('e.pyc', '4')
checkAdd('f.png', '5')
checkAdd('Backup.pyc', '6')
checkAdd('g.gif', '7')
checkAdd('h.pyc', '8')


# Main window
class Win2:
    def run(self):
        # Variable
        self.usbChoiceList = []
        self.startUpChoice = False
        # Main window
        self.win = Tk()
        self.win.title("Easy USB Backup")
        self.win.geometry('700x500')
        self.win.iconbitmap(path + 'material/a.ico')
        self.win.resizable(0, 0)
        self.win.option_add('*tearOff', False)

#==================================================================================================
        # Menu functions
        def Control():
            # Variable
            self.config1 = 0
            self.config2 = 0
            # Control window
            self.conWin = Tk()
            self.conWin.title("控制中心")
            self.conWin.iconbitmap(path + 'material/a.ico')
            self.conWin.geometry("710x80")
            self.conWin.resizable(0, 0)
            # Label
            self.conl1 = Label(self.conWin, text="检测时间间隔(s)", font=('fangsong', 13))
            self.conl2 = Label(self.conWin, text="备份文件夹命名方式", font=('fangsong', 13))
            self.conl3 = Label(self.conWin, text="检测到U盘插入时是否提示", font=('fangsong', 13))
            # Entry
            self.cone1 = Entry(self.conWin, width=64)

            # Radiobutton functions
            def conr1f():
                if self.config1 != 0:
                    self.conrL1 = [self.conr1, self.conr2, self.conr3, self.conr4]
                    self.conrL1[self.config1].deselect()
                    self.config1 = 0
                else:
                    self.conrL1[self.config1].select()

            def conr2f():
                if self.config1 != 1:
                    self.conrL1 = [self.conr1, self.conr2, self.conr3, self.conr4]
                    self.conrL1[self.config1].deselect()
                    self.config1 = 1
                else:
                    self.conrL1[self.config1].select()

            def conr3f():
                if self.config1 != 2:
                    self.conrL1 = [self.conr1, self.conr2, self.conr3, self.conr4]
                    self.conrL1[self.config1].deselect()
                    self.config1 = 2
                else:
                    self.conrL1[self.config1].select()

            def conr4f():
                if self.config1 != 3:
                    self.conrL1 = [self.conr1, self.conr2, self.conr3, self.conr4]
                    self.conrL1[self.config1].deselect()
                    self.config1 = 3
                else:
                    self.conrL1[self.config1].select()

            def conr7f():
                if self.config2 != 0:
                    self.conrL2 = [self.conr7, self.conr8]
                    self.conrL2[self.config2].deselect()
                    self.config2 = 0
                else:
                    self.conrL2[self.config2].select()

            def conr8f():
                if self.config2 != 1:
                    self.conrL2 = [self.conr7, self.conr8]
                    self.conrL2[self.config2].deselect()
                    self.config2 = 1
                else:
                    self.conrL2[self.config2].select()

            # Checkbutton
            self.conr1 = Checkbutton(self.conWin, text="时间", command=conr1f)
            self.conr2 = Checkbutton(self.conWin, text="U盘名称", command=conr2f)
            self.conr3 = Checkbutton(self.conWin, text="时间+U盘名称", command=conr3f)
            self.conr4 = Checkbutton(self.conWin, text="U盘名称+时间", command=conr4f)
            self.conr7 = Checkbutton(self.conWin, text="是", command=conr7f)
            self.conr8 = Checkbutton(self.conWin, text="否", command=conr8f)

            # Button fuctions
            def apply():
                Log("Apply button is clicked")
                try:
                    self.time = int(self.cone1.get())
                    self.jsconfig = {'time':self.time, 'config1':self.config1, 'config2':self.config2}
                    with open(path + 'info/config.json', encoding='utf-8') as fileConf:
                        fileConff = fileConf.readlines()
                    if fileConff == []:
                        with open(path + 'info/config.json', mode='w', encoding='utf-8') as f:
                            dump(self.jsconfig, f, indent=4, separators=(',', ':'))
                        if (messagebox.showinfo("控制中心", "应用成功")) == "ok":
                            self.conWin.destroy()
                    elif fileConff != []:
                        with open(path + 'info/config.json', encoding='utf-8') as f:
                            self.ff = load(f)
                        self.ff["time"] = self.time
                        self.ff['config1'] = self.config1
                        self.ff['config2'] = self.config2
                        with open(path + 'info/config.json', mode='w', encoding='utf-8') as f:
                            dump(self.ff, f, indent=4, separators=(",", ":"))
                        if (messagebox.showinfo("控制中心", "应用成功")) == "ok":
                            self.conWin.destroy()
                except:
                    messagebox.showerror("控制中心", "您输入的数据错误,或您打开了多个控制中心窗口.")

            def advice():
                Log("Advice button is clicked")
                self.cone1.delete(0, END)
                self.cone1.insert('insert', '2')
                self.conrL1 = [self.conr1, self.conr2, self.conr3, self.conr4]
                self.conrL1[self.config1].deselect()
                self.conr3.select()
                self.config1 = 2
                self.conrL2 = [self.conr7, self.conr8]
                self.conrL2[self.config2].deselect()
                self.conr8.select()
                self.config2 = 1

            # Button
            self.conb1 = Button(self.conWin, text="应用", relief=GROOVE, width=7, command=apply)
            self.conb2 = Button(self.conWin, text="推荐设置", relief=GROOVE, width=7, command=advice)
            # Display
            self.conl1.place(x=0, y=0)
            self.cone1.place(x=250, y=2)
            self.conl2.place(x=0, y=25)
            self.conr1.place(x=170, y=25)
            self.conr2.place(x=220, y=25)
            self.conr3.place(x=290, y=25)
            self.conr4.place(x=393, y=25)
            self.conl3.place(x=0, y=50)
            self.conr7.place(x=210, y=50)
            self.conr8.place(x=245, y=50)
            self.conb1.place(x=580, y=48)
            self.conb2.place(x=640, y=48)
            self.conWin.mainloop()
#==================================================================================================

        def About():
            # About window
            self.aboutwin = Toplevel()
            self.aboutwin.title("关于")
            self.aboutwin.geometry("300x200")
            self.aboutwin.resizable(0, 0)
            self.aboutwin.iconbitmap(path + 'material/a.ico')
            # Label
            self.aboutl1 = Label(self.aboutwin, text="Easy USB Backup", font=('Arial', 16))
            self.aboutl2 = Label(self.aboutwin, text="作者：Skyler Sun", font=('fangsong', 14))
            self.aboutl3 = Label(self.aboutwin, text="GUI设计：徐笳棋", font=('fangsong', 14))
            self.aboutl4 = Label(self.aboutwin, text="版本号：0-4", font=('fangsong', 14))
            # Display
            self.aboutl1.pack(side='top')
            self.aboutl2.place(x=15, y=30)
            self.aboutl3.place(x=15, y=55)
            self.aboutl4.place(x=15, y=80)
            self.aboutwin.mainloop()

#==================================================================================================
        # Menu
        self.winMenubar = Menu(self.win)
        self.winmenu = Menu(self.winMenubar)
        self.winmenu.add_command(label="控制中心", command=Control)
        self.winmenu.add_command(label="关于", command=About)
        self.winMenubar.add_cascade(label="设置", menu=self.winmenu)
        self.win['menu'] = self.winMenubar
        # Background
        self.backgroundImg = PhotoImage(file=path + 'material/g.gif')
        self.canvas = Canvas(width=700, height=480, highlightthickness=0, borderwidth=0)
        self.canvas.create_image(0, 0, image=self.backgroundImg, anchor='nw')
        # Label
        self.canvas.create_text(135, 25, text="选择U盘(可移动DISK)", font=('Arial', 17), fill='red')
        self.canvas.create_text(70, 365, text="备份位置", font=('Arial Black', 17), fill='red')
        self.canvas.create_text(590, 440, text="By: Skyler Sun", font=('Arial Black', 17), fill='white')
        self.location = Label(self.win, width=34, height=1, font=('fangsong', 17), anchor='w')
        # Frame
        self.usbFrame = Frame(self.win)
        # Text
        self.usbText = Text(self.usbFrame, height=23, width=67)

        # Checkbutton fuctioins
        def usbAct(content):
            if content in self.usbChoiceList:
                self.usbChoiceList.remove(content)
                Log(content + " disk is removed")
            elif content not in self.usbChoiceList:
                Log(content + " disk is added")
                self.usbChoiceList.append(content)
            self.usbChoiceList.sort()
            with open(path + 'info/config.json', encoding='utf-8') as f:
                ff = f.readlines()
            if ff != []:
                with open(path + 'info/config.json', encoding='utf-8') as F:
                    i = load(F)
                i['usbChoiceList'] = str(self.usbChoiceList)
                with open(path + 'info/config.json', mode='w', encoding='utf-8') as F:
                    dump(i, F, indent=4, separators=(',', ':'))
                Log("USB Choice List: " + str(self.usbChoiceList))
            elif ff == []:
                self.dict = {"usbChoiceList":str(self.usbChoiceList)}
                with open(path + 'info/config.json', mode='w', encoding='utf-8') as F:
                    dump(self.dict, F, indent=4, separators=(",", ":"))

        def usbDf():
            usbAct('D')

        def usbEf():
            usbAct('E')

        def usbFf():
            usbAct('F')

        def usbGf():
            usbAct('G')

        def usbHf():
            usbAct('H')

        def usbIf():
            usbAct('I')

        def usbJf():
            usbAct('J')

        def usbKf():
            usbAct('K')

        def usbLf():
            usbAct('L')

        def usbMf():
            usbAct('M')

        def usbNf():
            usbAct('N')

        def usbOf():
            usbAct('O')

        def usbPf():
            usbAct('P')

        def usbQf():
            usbAct('Q')

        def usbRf():
            usbAct('R')

        def usbSf():
            usbAct('S')

        def usbTf():
            usbAct('T')

        def usbUf():
            usbAct('U')

        def usbVf():
            usbAct('V')

        def usbWf():
            usbAct('W')

        def usbXf():
            usbAct('X')

        def usbYf():
            usbAct('Y')

        def usbZf():
            usbAct('Z')

        # Checkbutton
        self.usbD = Checkbutton(self.usbText, text="D盘", bg='white', command = usbDf)
        self.usbE = Checkbutton(self.usbText, text="E盘", bg='white', command = usbEf)
        self.usbF = Checkbutton(self.usbText, text="F盘", bg='white', command = usbFf)
        self.usbG = Checkbutton(self.usbText, text="G盘", bg='white', command = usbGf)
        self.usbH = Checkbutton(self.usbText, text="H盘", bg='white', command = usbHf)
        self.usbI = Checkbutton(self.usbText, text="I盘", bg='white', command = usbIf)
        self.usbJ = Checkbutton(self.usbText, text="J盘", bg='white', command = usbJf)
        self.usbK = Checkbutton(self.usbText, text="K盘", bg='white', command = usbKf)
        self.usbL = Checkbutton(self.usbText, text="L盘", bg='white', command = usbLf)
        self.usbM = Checkbutton(self.usbText, text="M盘", bg='white', command = usbMf)
        self.usbN = Checkbutton(self.usbText, text="N盘", bg='white', command = usbNf)
        self.usbO = Checkbutton(self.usbText, text="O盘", bg='white', command = usbOf)
        self.usbP = Checkbutton(self.usbText, text="P盘", bg='white', command = usbPf)
        self.usbQ = Checkbutton(self.usbText, text="Q盘", bg='white', command = usbQf)
        self.usbR = Checkbutton(self.usbText, text="R盘", bg='white', command = usbRf)
        self.usbS = Checkbutton(self.usbText, text="S盘", bg='white', command = usbSf)
        self.usbT = Checkbutton(self.usbText, text="T盘", bg='white', command = usbTf)
        self.usbU = Checkbutton(self.usbText, text="U盘", bg='white', command = usbUf)
        self.usbV = Checkbutton(self.usbText, text="V盘", bg='white', command = usbVf)
        self.usbW = Checkbutton(self.usbText, text="W盘", bg='white', command = usbWf)
        self.usbX = Checkbutton(self.usbText, text="X盘", bg='white', command = usbXf)
        self.usbY = Checkbutton(self.usbText, text="Y盘", bg='white', command = usbYf)
        self.usbZ = Checkbutton(self.usbText, text="Z盘", bg='white', command = usbZf)
        self.usbText.window_create('insert', window=self.usbD)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbE)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbF)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbG)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbH)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbI)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbJ)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbK)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbL)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbM)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbN)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbO)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbP)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbQ)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbR)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbS)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbT)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbU)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbV)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbW)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbX)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbY)
        self.usbText.insert('insert', '\n')
        self.usbText.window_create('insert', window=self.usbZ)
        # ScrollBar
        self.usbScrollBar = Scrollbar(self.usbFrame, width=20, orient='vertical')

        # Button fuction
        def throughf():
            self.copyTo = filedialog.askdirectory()
            with open(path + 'info/config.json', encoding='utf-8') as f:
                if f.readlines() == []:
                    with open(path + 'info/config.json', mode='w', encoding='utf-8') as F:
                        self.dict = {"copyTo":self.copyTo}
                        dump(self.dict, F, indent=4, separators=(",", ":"))
                else:
                    with open(path + 'info/config.json', encoding='utf-8') as F:
                        self.dict = load(F)
                    self.dict["copyTo"] = self.copyTo
                    with open(path + 'info/config.json', mode='w', encoding='utf-8') as F:
                        dump(self.dict, F, indent=4, separators=(",", ":"))
            self.copyToPath.set(self.copyTo)

        def startUpButtonf():
            if self.startUpChoice == False:
                Popen('copy ' + winPath + 'startup\\startup.exe "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp"', shell=True)
                with open('C:/Easy USB Backup Info.pyc', mode='w') as i:
                    i.write(winPath + "main.exe")
                Log("开机自启已选择")
                self.startUpText.set("开机自启")
                self.startUpChoice = True
            elif self.startUpChoice == True:
                Popen('del ' + '"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\startup.exe"', shell=True)
                Log("开机不自启已选择")
                self.startUpText.set("开机不自启")
                self.startUpChoice = False

        def Helpf():
            Log("Help window starts")
            # Help window
            self.helP = Toplevel()
            self.helP.geometry('500x318')
            self.helP.title('Easy USB Backup')
            self.helP.iconbitmap(path + 'material/a.ico')
            self.helP.resizable(0, 0)
            # Extensions
            self.helPBar = Scrollbar(self.helP, orient='vertical', width=20)
            self.helPText = Text(self.helP, width=68, yscrollcommand=self.helPBar.set)
            with open(path + 'material/h.pyc', encoding='utf-8') as file:
                helPContent = file.readlines()
            for i in helPContent:
                self.helPText.insert('insert', i)
            self.helPText.config(state='disabled')
            self.helPBar.config(command=self.helPText.yview)
            # Display
            self.helPText.place(x=0, y=0)
            self.helPBar.pack(side='right', fill='y')
            self.helP.mainloop()

        def Hidef():
            self.win.withdraw()
            messagebox.showinfo("Easy USB Backup", "窗口已隐藏，按下alt来还原窗口")
            def onPress(key):
                try:
                    i = []
                    i.append(str(key.char))
                    del i
                except AttributeError:
                    if str(key) == 'Key.alt_l':
                        self.win.deiconify()
                        listener.stop()
            def onRelease(key):
                pass
            listener = pynput.keyboard.Listener(on_press=onPress, on_release=onRelease)
            listener.start()

        def LogLook():
            Popen('"' + winPath + 'Easy USB Backup.log"', shell=True)

        def Killf():
            Popen('taskkill /f /im main.exe', shell=True)

        def BackupLook():
            try:
                i1 = -1
                i = list(self.copyTo)
                for I in i:
                    i1 += 1
                    if I == "/":
                        i[i1] = "\\"
                i = ''.join(i)
                del i1
                Popen('explorer ' + i, shell=True)
                del i
            except:
                messagebox.showerror("Easy USB Backup", "请先选择备份目录")

        def Startf():
            if messagebox.showinfo("Easy USB Backup", "   程序已开始, 请勿多次点击开始备份按钮") == 'ok':

                def BackupRun():
                    with open(path + 'info/config.json', encoding='utf-8') as f:
                        q = f.readlines()
                    if q == []:
                        Log("Json file is empty")
                        messagebox.showerror("Easy USB Backup", "   设置错误   ")
                    else:
                        Log("Json file has items")
                        with open(path + 'info/config.json', encoding='utf-8') as f:
                            i = load(f)
                        order = 1
                        try:
                            time = i['time']
                            config1 = i['config1']
                            config2 = i['config2']
                            copyTo = i['copyTo']
                            usbChoiceList = list(i['usbChoiceList'])
                            order = 0
                        except:
                            Log("Json file is not currect")
                            messagebox.showerror("Easy USB Backup", "   设置错误   ")
                        if list(copyTo)[-1] != '/':
                            copyTo += '/'
                        if order == 0:
                            usbChoiceList.remove('[')
                            usbChoiceList.remove(']')
                            # change list
                            def ChangeUSBList(content):
                                while True:
                                    try:
                                        usbChoiceList.remove(content)
                                    except ValueError:
                                        break

                            ChangeUSBList("'")
                            ChangeUSBList(',')
                            ChangeUSBList(' ')
                            # check usbchoicelist
                            uusbChoiceList = usbChoiceList[:]
                            localDisks = []
                            order = -1
                            ordeR = 0
                            for i in disk_partitions():
                                if "removable" not in i.opts:
                                    localDisks.append(i.mountpoint)
                            for i in usbChoiceList:
                                order += 1
                                uusbChoiceList[order] += ':\\'
                                usbChoiceList[order] += ':/'
                                if uusbChoiceList[order] in localDisks:
                                    a = Tk()
                                    a.withdraw()
                                    Log("USB choice is wrong")
                                    messagebox.showerror("Easy USB Backup", "您选择的U盘有误, 请重新选择")
                                    a.destroy()
                                    ordeR = 1
                                    break
                            # Start to detect
                            if ordeR == 0:
                                # Variable
                                order1 = 1
                                copyedDevices = []
                                usbDevices = []
                                position1 = ''
                                position2 = ''

                                # thread function
                                def cpThf():
                                    if config2 == 0:
                                        if messagebox.showinfo('Easy USB Backup', '检测到有U盘插入') == 'ok':
                                            copyedDevices.append(position1)
                                            copytree(position1, position2)
                                    elif config2 == 1:
                                        copyedDevices.append(position1)
                                        copytree(position1, position2)

                                while True:
                                    Log('Start to detect USB')
                                    devices = disk_partitions()
                                    for device in devices:
                                        if "removable" in device.opts:
                                            mountpoint = list(device.mountpoint)[0] + ':/'
                                            usbDevices.append(mountpoint)
                                            order1 = 0
                                    if copyedDevices != []:
                                        for i in copyedDevices:
                                            if i not in usbDevices:
                                                copyedDevices.remove(i)
                                    if order1 == 0:
                                        Log('Found USB')
                                        # copy starts
                                        for device in usbDevices:
                                            if (device in usbChoiceList) and (device not in copyedDevices):
                                                position1 = device
                                                ddevice = list(device)
                                                ddevice.pop()
                                                ddevice = ''.join(ddevice)
                                                wwinPath = list(winPath)
                                                wwinPath[0] = wwinPath[0].upper()
                                                wwinPath = ''.join(wwinPath)
                                                Popen('vol ' + ddevice + ' > ' + wwinPath + 'info\\name.pyc', shell=True)
                                                sleep(3)
                                                # with open(path + 'info/name.pyc', encoding='unicode_escape') as f:
                                                with open(path + 'info/name.pyc', encoding = 'gbk') as f:
                                                    usbname = list(f.readlines()[0])
                                                usbName = []
                                                allow = -4
                                                for i in usbname:
                                                    if allow == 0:
                                                        if i != '\n':
                                                            usbName.append(i)
                                                    elif allow != 0:
                                                        if i == ' ':
                                                            allow += 1
                                                usbName = ''.join(usbName)
                                                if config1 == 0:
                                                    now = strftime('%Y-%m-%d  %H-%M-%S')
                                                    position2 = copyTo + now
                                                elif config1 == 1:
                                                    position2 = copyTo + usbName
                                                elif config1 == 2:
                                                    now = strftime('%Y-%m-%d  %H-%M-%S')
                                                    position2 = copyTo + now + ', ' + usbName
                                                elif config1 == 3:
                                                    now = strftime('%Y-%m-%d  %H-%M-%S')
                                                    position2 = copyTo + usbName + ', ' + now
                                                cpTh = Thread(target=cpThf, daemon=True)
                                                cpTh.start()
                                    usbDevices.clear()
                                    Log('End detect')
                                    sleep(time)

                BackupTh = Thread(target=BackupRun, daemon=True)
                BackupTh.start()

        # Button
        self.through = Button(self.win, text="浏览", command=throughf, relief=GROOVE, width=8)
        self.startUpButton = Button(self.win, font=('fangsong', 15), relief=GROOVE, command=startUpButtonf, width=10)
        self.helpButton = Button(self.win, text="使用必读", relief=GROOVE, width=10, font=('fangsong', 15), command=Helpf)
        self.hideButton = Button(self.win, text="隐藏", relief=GROOVE, width=10, font=('fangsong',15), command=Hidef)
        self.logButton = Button(self.win, text="日志文件", relief=GROOVE, width=10, font=('fangsong', 15), command=LogLook)
        self.killButton = Button(self.win, text="结束任务", relief=GROOVE, width=10, font=('fangsong', 15), command=Killf)
        self.BackupButton = Button(self.win, text="备份目录", relief=GROOVE, width=10, font=('fangsong', 15), command=BackupLook)
        self.startButton = Button(self.win ,text="开始备份", relief=GROOVE, width=10, font=('fangsong', 15), command=Startf)
        # Config
        self.usbText.config(state='disabled', cursor='arrow')
        self.usbText.configure(yscrollcommand=self.usbScrollBar.set)
        self.usbScrollBar.config(command=self.usbText.yview)
        # Display
        # StartUpButton
        self.startUpButton.place(x=540, y=50)
        self.startUpText = StringVar()
        self.startUpText.set("开机不自启")
        self.startUpButton.config(textvariable=self.startUpText)
        # Location
        self.location.place(x=19, y=380)
        self.copyToPath = StringVar()
        self.location.config(textvariable=self.copyToPath)
        # Others
        self.through.place(x=443, y=380)
        self.usbText.pack(side='left')
        self.usbScrollBar.pack(side='right', fill='y')
        self.canvas.place(x=0, y=0)
        self.usbFrame.place(x=19, y=45)
        self.helpButton.place(x=540, y=100)
        self.hideButton.place(x=540, y=150)
        self.logButton.place(x=540, y=200)
        self.killButton.place(x=540, y=250)
        self.BackupButton.place(x=540, y=300)
        self.startButton.place(x=540, y=350)
        # Loop
        self.win.mainloop()
        Log("=========Program ends=========")

# Content window
class Win1:
    def run(self):
        # Var set
        self.choice1 = "No"
        self.choice2 = None
        self.donateo = 0
        self.donateol = []
        # Window set
        self.win = Tk()
        self.win.title("Easy USB Backup")
        self.win.geometry('700x400')
        self.win.resizable(0, 0)
        self.win.iconbitmap(path + 'material/a.ico')
        # Background
        self.canvas = Canvas(width=700, height=400, highlightthickness=0, borderwidth=0)
        self.background = PhotoImage(file=path + 'material/b.gif')
        self.canvas.create_image(0, 0, image=self.background, anchor='nw')
        # Ico
        self.ico = PhotoImage(file=path + 'material/c.png')
        self.canvasIco = Canvas(width=260, height=244, highlightthickness=0, borderwidth=0)
        self.canvasIco.create_image(0, 0, image=self.ico, anchor='nw')
        # Label
        self.l1 = self.canvas.create_text(350, 260, font=('Arial Black', 20))
        self.l2 = self.canvas.create_text(520, 365, font=('Arial Black', 17))

        # Button functions
        def b1f():
            if self.choice2 == True:
                self.win.destroy()
                Log("Content window is closed")
                self.win2 = Win2()
                Log("=========Start to run main window=========")
                self.win2.run()
            elif self.choice2 == None:
                messagebox.showwarning("Easy USB Backup", "请先点击软件协议")

        def b2f():
            Log("Start to run agreement window")
            if self.choice2 != True:
                self.rule = Toplevel()
                self.rule.title('Easy USB Backup')
                self.rule.geometry('500x350')
                self.rule.resizable(0, 0)
                self.rule.iconbitmap(path + 'material/a.ico')
                # Extensions
                self.ruleBar = Scrollbar(self.rule, orient='vertical', width=20)
                self.ruleText = Text(self.rule, width=68, yscrollcommand=self.ruleBar.set)
                with open(path + 'material/d.pyc', encoding='utf-8') as file:
                    ruleContent = file.readlines()
                for i in ruleContent:
                    self.ruleText.insert('insert', i)
                del i
                self.ruleBar.config(command=self.ruleText.yview)
                self.ruleText.config(state='disabled')

                def ruleB1f():
                    if self.choice1 == "No":
                        self.choice1 = "Yes"
                    elif self.choice1 == "Yes":
                        self.choice1 = "No"

                def ruleB2f():
                    if self.choice1 == "Yes":
                        Log("Agreement is accessed")
                        self.rule.destroy()
                        messagebox.showinfo("Easy USB Backup", "感谢您对本软件的信赖,祝您使用愉快!")
                        self.choice2 = True
                    elif self.choice1 == "No":
                        messagebox.showerror("Easy USB Backup", "请认真仔细阅读该软件协议!")

                def ruleB3f():
                    if self.choice1 == "Yes":
                        Log("Agreement is refused, start to exit")
                        sys.exit()
                    elif self.choice1 == "No":
                        messagebox.showerror("Easy USB Backup", "请认真仔细阅读该软件协议!")

                self.ruleB1 = Checkbutton(self.rule, text="我已仔细认真阅读以上软件协议", command=ruleB1f)
                self.ruleB2 = Button(self.rule, text="我同意以上软件协议", command = ruleB2f, relief=GROOVE)
                self.ruleB3 = Button(self.rule, text="我拒绝以上软件协议", command = ruleB3f, relief=GROOVE)
                # Display
                self.ruleText.place(x=0, y=0)
                self.ruleBar.pack(side='right', fill='y')
                self.ruleB1.place(x=0, y=320)
                self.ruleB2.place(x=200, y=318)
                self.ruleB3.place(x=340, y=318)
                self.rule.mainloop()

        def b3f():
            if self.choice2 == True:
                Log("Button update is clicked")
                web.open("https://github.com/Skyler-std/program_py/tree/main/USB_copy", new=2, autoraise=True)
            elif self.choice2 == None:
                messagebox.showwarning("Easy USB Backup", "请先点击软件协议")

        def b4f():
            if self.choice2 == True:
                Log("Tip button is clicked")
                # Tip window
                self.tip = Toplevel()
                self.tip.geometry('500x318')
                self.tip.title("Easy USB Backup")
                self.tip.iconbitmap(path + 'material/a.ico')
                self.tip.resizable(0, 0)
                # Extensions
                self.tipBar = Scrollbar(self.tip, orient='vertical', width=20)
                self.tipText = Text(self.tip, width=68, yscrollcommand=self.tipBar.set)
                with open(path + 'material/e.pyc', encoding='utf-8') as file:
                    tipContent = file.readlines()
                for i in tipContent:
                    self.tipText.insert('insert', i)
                self.tipText.config(state='disabled')
                self.tipBar.config(command=self.tipText.yview)
                # Display
                self.tipText.place(x=0, y=0)
                self.tipBar.pack(side='right', fill='y')
                self.tip.mainloop()
            elif self.choice2 == None:
                messagebox.showwarning("Easy USB Backup", "请先点击软件协议")

        def b5f():
            if self.choice2 == True:
                Log("Donate button is clicked")
                self.donateo += 1
                self.donateol.append(self.donateo)
                if len(self.donateol) == 1:

                    def donateThf():
                        pygame.init()
                        self.icon = pygame.image.load(path + 'material/a.ico')
                        pygame.display.set_icon(self.icon)
                        self.screen = pygame.display.set_mode((399, 399))
                        pygame.display.set_caption("Easy USB Backup")
                        self.donateImg = pygame.image.load(path + 'material/f.png').convert()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    self.donateol.clear()
                                    return
                            self.screen.blit(self.donateImg, (-1, -1))
                            pygame.display.update()

                    self.donateTh = Thread(target=donateThf, daemon=False)
                    self.donateTh.start()

            elif self.choice2 == None:
                messagebox.showwarning("Easy USB Backup", "请先点击软件协议")

        def b6f():
            if self.choice2 == True:
                Log("Contact button is clicked")
                # Contact Window
                self.connect = Toplevel()
                self.connect.title("Easy USB Backup")
                self.connect.iconbitmap(path + 'material/a.ico')
                self.connect.geometry('500x350')
                self.connect.resizable(0, 0)
                # Extensions
                self.connectT = Text(self.connect, width=500, height=350)
                self.connectT.insert('insert', 'QQ:3385213313\nWechat id:wxid-ZhanChiPengFei')
                self.connectT.config(state='disabled')
                # Display
                self.connectT.place(x=0, y=0)
                self.connect.mainloop()
            elif self.choice2 == None:
                messagebox.showwarning("Easy USB Backup", "请先点击软件协议")

        # Button
        self.b1 = Button(self.win, font=('Arial Black', 14), width=10, height=1, relief=GROOVE, text='主界面', command=b1f)
        self.b2 = Button(self.win, font=('Arial Black', 14), width=10, height=1, relief=GROOVE, text='软件协议', command=b2f)
        self.b3 = Button(self.win, font=('Arial Black', 14), width=10, height=1, relief=GROOVE, text='检查更新', command=b3f)
        self.b4 = Button(self.win, font=('Arial Black', 14), width=10, height=1, relief=GROOVE, text='注意事项', command=b4f)
        self.b5 = Button(self.win, font=('Arial Black', 14), width=10, height=1, relief=GROOVE, text='捐赠', command=b5f)
        self.b6 = Button(self.win, font=('Arial Black', 14), width=10, height=1, relief=GROOVE, text='联系方式', command=b6f)
        # Loop
        self.canvas.place(x=0, y=0)
        self.canvas.insert(self.l1, 1, "Easy USB Backup")
        self.canvas.insert(self.l2, 1, "您的支持乃作者的最大动力")
        self.canvasIco.place(x=220, y=0)
        self.X = 20
        self.Y = 290
        self.b1.place(x=self.X, y=self.Y)
        self.b2.place(x=self.X + 170, y=self.Y)
        self.b3.place(x=self.X + 340, y=self.Y)
        self.b4.place(x=self.X + 510, y=self.Y)
        self.b5.place(x=self.X, y=self.Y + 55)
        self.b6.place(x=self.X + 170, y=self.Y + 55)
        self.win.mainloop()

if __name__ == '__main__':
    order = 0
    for i in checkL:
        if 'False' in i:
            order = 1
            temp = Tk()
            temp.withdraw()
            messagebox.showerror("Error!", "File " + checkNl[int(list(i)[-1])] + " is not found!!!")
            temp.destroy()
    if order == 1:
        sys.exit()
    try:
        file = open(path + 'info/config.json')
        file.close()
    except FileNotFoundError:
        temp = Tk()
        temp.withdraw()
        messagebox.showerror('Error!', 'File ' + winPath + 'info\\config.json Not Found!!!')
        temp.destroy()
        sys.exit()
    Log("Check ends")
    with open(path + 'info/config.json', mode='w', encoding='utf-8') as f:
        pass
    del f
    win1 = Win1()
    Log("=========Start to run content window=========")
    win1.run()
