#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: ChengBingBing

import time,threading
import datetime
import re


class Filter:
    def __init__(self):
        with open('filter.ini',"r", encoding=('utf-8')) as filter_file:    #设置文件对象
            self.line = filter_file.readlines()
            self.step = 0
            self.func_filter = []
            self.set_reg_single_id_filter = []
            self.set_reg_range_id_filter = []
            self.set_str_reg_single_id_filter = []
            self.set_str_reg_range_id_filter = []
            self.get_reg_single_id_filter = []
            self.get_reg_range_id_filter = []
            self.resp_reg_single_id_filter = []
            self.resp_reg_range_id_filter = []
            self.out_reg_id = []
            self.out_reg_value = []

            for line in self.line:
                if (line[0] == '#'):
                    continue

                if 'FUNC_FILTER:' in line:
                    self.step = 1
                    continue
                elif 'SET_REG_ID_FILTER:' in line:
                    self.step = 2
                    continue
                elif 'GET_REG_ID_FILTER:' in line:
                    self.step = 3
                    continue
                elif 'SET_STR_REG_ID_FILTER:' in line:
                    self.step = 4
                    continue
                elif 'RESP_REG_ID_FILTER:' in line:
                    self.step = 5
                    continue

                if self.step == 1:
                    if 'SET_REG' in line:
                        self.func_filter.append("SET_REG")
                    elif 'GET_REG'in line:
                        self.func_filter.append("GET_REG")
                    elif 'SET_STR_REG'in line:
                        self.func_filter.append("SET_STR_REG")
                    elif 'RESP_REG' in line:
                        self.func_filter.append("RESP_REG")
                    elif 'RESP_STATE'in line:
                        self.func_filter.append("RESP_STATE")
                elif self.step == 2:
                    num = re.findall(r'\d+', line)
                    if len(num) == 1:
                        self.set_reg_single_id_filter.append(int(num[0]))
                    elif len(num) == 2:
                        self.set_reg_range_id_filter.append(int(num[0]))
                        self.set_reg_range_id_filter.append(int(num[1]))
                elif self.step == 3:
                    num = re.findall(r'\d+', line)
                    if len(num) == 1:
                        self.get_reg_single_id_filter.append(int(num[0]))
                    elif len(num) == 2:
                        self.get_reg_range_id_filter.append(int(num[0]))
                        self.get_reg_range_id_filter.append(int(num[1]))
                elif self.step == 4:
                    num = re.findall(r'\d+', line)
                    if len(num) == 1:
                        self.set_str_reg_single_id_filter.append(int(num[0]))
                    elif len(num) == 2:
                        self.set_str_reg_range_id_filter.append(int(num[0]))
                        self.set_str_reg_range_id_filter.append(int(num[1]))
                elif self.step == 5:
                    num = re.findall(r'\d+', line)
                    if len(num) == 1:
                        self.resp_reg_single_id_filter.append(int(num[0]))
                    elif len(num) == 2:
                        self.resp_reg_range_id_filter.append(int(num[0]))
                        self.resp_reg_range_id_filter.append(int(num[1]))
                else:
                    pass

            filter_file.close()

    def recv_filter(self, time, func = "SET_REG", id =[], value=[], state=0, frame_err=0, reg_err = []):
        for str in self.func_filter:
            if func in str:
                return

        #print(self.out_reg_id)
        #print(self.out_reg_value)
        #self.out_reg_id.clear()
        #self.out_reg_value.clear()
        #print(self.out_reg_id)
        #print(self.out_reg_value)

        if func == "SET_REG":
            if (len(id) == 0) or (len(value) == 0):
                return

            self.out_reg_id = id
            self.out_reg_value = value

            # 单寄存器ID过滤
            for i in self.set_reg_single_id_filter:
                cnt = 0
                while cnt < len(self.out_reg_id):
                    if i == self.out_reg_id[cnt]:
                        self.out_reg_id.pop(cnt)
                        self.out_reg_value.pop(cnt)
                        continue
                    else:
                        cnt += 1
            # 指定范围寄存器ID过滤
            for i in range(int(len(self.set_reg_range_id_filter)/2)):
                cnt = 0
                while cnt < len(self.out_reg_id):
                    if (self.out_reg_id[cnt] >= self.set_reg_range_id_filter[2*i]) and (self.out_reg_id[cnt] <= self.set_reg_range_id_filter[2*i+1]):
                        self.out_reg_id.pop(cnt)
                        self.out_reg_value.pop(cnt)
                    else:
                        cnt += 1

            if len(self.out_reg_id) != 0:
                print("[" + time + "]" + " [" + func + "] -> ", end="")
                for i in range(len(self.out_reg_id)):
                    print("<", end="")
                    print(self.out_reg_id[i], end="")
                    print(": ", end="")
                    print(self.out_reg_value[i], end="")
                    print("> ", end="")
                print("\r")

        elif func == "GET_REG":
            if len(id) == 0:
                return

            self.out_reg_id = id
            # 单寄存器ID过滤
            for i in self.get_reg_single_id_filter:
                cnt = 0
                while cnt < len(self.out_reg_id):
                    if i == self.out_reg_id[cnt]:
                        self.out_reg_id.pop(cnt)
                        continue
                    else:
                        cnt += 1
            # 指定范围寄存器ID过滤
            for i in range(int(len(self.get_reg_range_id_filter)/2)):
                cnt = 0
                while cnt < len(self.out_reg_id):
                    if (self.out_reg_id[cnt] >= self.get_reg_range_id_filter[2*i]) and (self.out_reg_id[cnt] <= self.get_reg_range_id_filter[2*i+1]):
                        self.out_reg_id.pop(cnt)
                    else:
                        cnt += 1

            if len(self.out_reg_id) != 0:
                print("[" + time + "]" + " [" + func + "] -> ", end="")
                for i in range(len(self.out_reg_id)):
                    print("<", end="")
                    print(self.out_reg_id[i], end="")
                    print("> ", end="")
                print("\r")

        elif func == "SET_STR_REG":
            if (len(id) == 0) or (len(value) == 0):
                return

            self.out_reg_id = id
            self.out_reg_value = value
            # 单寄存器ID过滤
            for i in self.set_str_reg_single_id_filter:
                cnt = 0
                while cnt < len(self.out_reg_id):
                    if i == self.out_reg_id[cnt]:
                        self.out_reg_id.pop(cnt)
                        self.out_reg_value.pop(cnt)
                        continue
                    else:
                        cnt += 1
            # 指定范围寄存器ID过滤
            for i in range(int(len(self.set_str_reg_range_id_filter)/2)):
                cnt = 0
                while cnt < len(self.out_reg_id):
                    if (self.out_reg_id[cnt] >= self.set_str_reg_range_id_filter[2*i]) and (self.out_reg_id[cnt] <= self.set_str_reg_range_id_filter[2*i+1]):
                        self.out_reg_id.pop(cnt)
                        self.out_reg_value.pop(cnt)
                    else:
                        cnt += 1

            if len(self.out_reg_id) != 0:
                print("[" + time + "]" + " [" + func + "] -> ", end="")
                for i in range(len(self.out_reg_id)):
                    print("<", end="")
                    print(self.out_reg_id[i], end="")
                    print(": ", end="")
                    print(self.out_reg_value[i], end="")
                    print("> ", end="")
                print("\r")
        elif func == "RESP_REG":
            if (len(id) == 0) or (len(value) == 0):
                return

            self.out_reg_id = id
            self.out_reg_value = value
            # 单寄存器ID过滤
            for i in self.resp_reg_single_id_filter:
                cnt = 0
                while cnt < len(self.out_reg_id):
                    if i == self.out_reg_id[cnt]:
                        self.out_reg_id.pop(cnt)
                        self.out_reg_value.pop(cnt)
                        continue
                    else:
                        cnt += 1
            # 指定范围寄存器ID过滤
            for i in range(int(len(self.resp_reg_range_id_filter)/2)):
                cnt = 0
                while cnt < len(self.out_reg_id):
                    if (self.out_reg_id[cnt] >= self.resp_reg_range_id_filter[2*i]) and (self.out_reg_id[cnt] <= self.resp_reg_range_id_filter[2*i+1]):
                        self.out_reg_id.pop(cnt)
                        self.out_reg_value.pop(cnt)
                    else:
                        cnt += 1

            if len(self.out_reg_id) != 0:
                print("[" + time + "]" + " [" + func + "] -> ", end="")
                for i in range(len(self.out_reg_id)):
                    print("<", end="")
                    print(self.out_reg_id[i], end="")
                    print(": ", end="")
                    print(self.out_reg_value[i], end="")
                    print("> ", end="")
                print("\r")
        elif func == "RESP_STATE":
            print("[" + time + "]" + " [" + func + "] -> <State: ", end="")
            print(hex(state), end="")
            print(", FrameErr: " + hex(frame_err) + ">", end="")
            print(" <RegOperaErr: ", end="")
            for i in range(len(reg_err)):
                print(hex(reg_err[i]), end="")
                print(" ", end="")
            print("> ", end="")
            print("\r")


if '__main__' == __name__:
    filter = Filter()
    reg_id = [1,2,3,4,5,6,7,8,9,10]
    value = [1,2,3,4,5,6,7,8,9,10]
    filter.recv_filter(datetime.datetime.now().strftime('%H:%M:%S.%f'), "RESP_STATE", frame_err=12,state=13, reg_err=reg_id)
##    print("set_str_reg_filter: " + str(filter.set_str_reg_filter))
##    print("get_reg_filter: " + str(filter.get_reg_filter))
##    print("resp_reg_filter: " + str(filter.resp_reg_filter))
##    print("resp_state_filter: " + str(filter.resp_state_filter))
##
##    print("set_reg_single_id_filter: ", end="")
##    for i in filter.set_reg_single_id_filter:
##        print(i, end="")
##    print("\r\n")
##    print("set_reg_range_id_filter: ", end="")
##    for i in filter.set_reg_range_id_filter:
##        print(i, end="")
##    print("\r\n")
##    print("set_str_reg_single_id_filter: ", end="")
##    for i in filter.set_str_reg_single_id_filter:
##        print(i, end="")
##    print("\r\n")
##    print("set_str_reg_range_id_filter: ", end="")
##    for i in filter.set_str_reg_range_id_filter:
##        print(i, end="")
##    print("\r\n")
##    print("get_reg_single_id_filter: ", end="")
##    for i in filter.get_reg_single_id_filter:
##        print(i, end="")
##    print("\r\n")
##    print("get_reg_range_id_filter: ", end="")
##    for i in filter.get_reg_range_id_filter:
##        print(i, end="")
##    print("\r\n")
##    print("resp_reg_single_id_filter: ", end="")
##    for i in filter.resp_reg_single_id_filter:
##        print(i, end="")
##    print("\r\n")
##    print("resp_reg_range_id_filter: ", end="")
##    for i in filter.resp_reg_range_id_filter:
##        print(i, end="")
##    print("\r\n")
