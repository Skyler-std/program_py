#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import system


# START
# 程序开始
system("pip list --outdated>pip_update_pyoutdated.txt")

# 保存pip库过期的信息为file_content
with open("pip_update_pyoutdated.txt") as file:
    file_content = file.readlines()

# 删除文件的不必要内容
for i in range(2):
    file_content.pop(0)

Pip_content = ""
Pip_content_l = []

for pip_content in file_content:

    for i in pip_content:
        if i == " ":
            Pip_content_l.append(Pip_content)
            Pip_content = ""
            break
        
        Pip_content += i

for pip_update in Pip_content_l:
    system("pip install --upgrade " + pip_update)