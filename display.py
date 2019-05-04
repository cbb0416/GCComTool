#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: ChengBingBing

import tkinter
import threading
import demjson

class Display(object):
    _instance_lock = threading.Lock()
    root = None

    def __init__(self):
        if root == None:
            print("root is None, error!!!")

    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(Display, "_instance"):
            with Display._instance_lock:
                if not hasattr(Display, "_instance"):
                    Display._instance = object.__new__(cls)
                    root = tkinter.Tk()
                    root.title("123")
                    root.mainloop()
        return Display._instance

if '__main__' == __name__:
    disp = Display()
    disp1 = Display()

