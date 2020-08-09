#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/4/25 22:17
# @File   : main.py
# -----------------------------------------------

import time

if __name__ == '__main__':
    with open('./test.dat', 'a+') as file :
        file.write(time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime()))
        
