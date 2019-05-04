#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: ChengBingBing

import demjson
import os

class Config(object):
    def __init__(self):
        self.dict = {}
        self.default_dict = {
            "VERSION": 1.0,
            "COM_NUM": 1,
            "COM1_PORT": "COM1"
            }
        self.default_version = "1.0"

        self.default_com_num = 0
        self.default_com_port = 0
        self.default_com_name = "COM"
        self.default_com_baudrate = 115200

    def read(self):
        try:
            with open("config.json", mode='r+', encoding='utf-8') as ff:
                size = os.path.getsize("config.json")
                if size == 0: #文件为空
                    self.set_default()
                    self.dict = self.default_dict.copy()
                    data = demjson.encode(self.dict)
                    ff.write(data)
                    ff.close()
                else:
                    data = ff.read()
                    self.dict = demjson.decode(data)
                    print(self.dict)

        except FileNotFoundError:
            with open("config.json", mode='w', encoding='utf-8') as ff:
                self.set_default()
                self.dict = self.default_dict.copy()
                data = demjson.encode(self.dict)
                ff.write(data)
                ff.close()

    def write(self, data):
        try:
            with open("config.json", mode='r', encoding='utf-8') as ff:
                ff = demjson.encode(data)
                ff.close()
        except FileNotFoundError:
            with open("config.json", mode='w', encoding='utf-8') as ff:
                self.set_default()
                self.dict = self.default_dict.copy()
                ff = demjson.encode(self.dict)
                ff.close()

    def set_default(self):
        self.default_dict['VERSION'] = self.default_version

if '__main__' == __name__:
    config = Config()
    config.read()