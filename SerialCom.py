#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: ChengBingBing

import serial
import serial.tools.list_ports
import time,threading
import datetime
from ComProtocol import ComMaster, ComSlave, ComProtocol

class SerialCom:
##    def prn_obj(self, obj):
##        print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))
        
    def __init__(self, com, m_or_s, baudrate=115200):
        self.com = object
        self.m_or_s = m_or_s
        self.recv_buffer = []
        #搜索所有可用的串口号
        plist = list(serial.tools.list_ports.comports())
        for i in plist:
            #print(i)
            plist_0 = list(i)
            print(plist_0[0])
            if com == plist_0[0]:
                self.com = serial.Serial(com, baudrate)
                if m_or_s == "master":
                    self.prot = ComMaster()
                    self.prot.debug_dis()
                    self.recv_head = 0x5A
                    self.trans_head = 0xA5
                elif m_or_s == "slave":
                    self.prot = ComSlave()
                    self.prot.debug_dis()
                    self.recv_head = 0xA5
                    self.trans_head = 0x5A
                else:
                    print(r'm_or_s err, please write "master" or "slave"!')
##        if self.com != object:
##            print("serial com create success")
##        else:
##            print("serial com create failed! not found port: " + com)

        #创建接收任务
        self.recv_task = threading.Thread(target=self.recv_task_func, name='recv task thread')
        self.recv_task.start()    
        
    def open(self):
        if self.com == object:
            return
        
        try:
            if self.com.isOpen() == False:
                print("open")
                self.com.open()
        except BaseException as e:
            print("open err：",e)

    def close(self):
        if self.com == object:
            return

        try:
            if self.com.isOpen() == True:
                print("close")
                self.com.close()
        except BaseException as e:
            print("close err：",e)

    def send(self, dat):
##        if self.com == object:
##            return
##        
##        if self.com.isOpen() == False:
##            return

        try:
            self.com.write(dat)
        except BaseException as e:
            self.close()
            print("send err：",e)

    def recv_task_func(self):
        try:
            while True:
                num = self.com.in_waiting
                    
                for dat in self.com.read(num):
                    #print(str(dat) + "\r\n")
                    #print("recv_buffer length: " + str(len(self.recv_buffer)) + "\r\n")
                    if (len(self.recv_buffer) == 0) and (dat == self.recv_head):
                        self.recv_buffer.append(dat)
                        #获取开始接收到数据的时间
                        self.recv_time = datetime.datetime.now().strftime('%H:%M:%S.%f')
##                        print(self.recv_time)
                    else:
                        if len(self.recv_buffer) != 0:
                            self.recv_buffer.append(dat)

                        if (len(self.recv_buffer) >= 7) and (dat == 0xC3):
                            func = self.recv_buffer[1] & 0x70
                            reg_num = self.recv_buffer[1] & 0x0F
                            reg_num += 1
##                            print(str(self.recv_buffer[1]) + " func: " + str(func) + " reg_num: " + str(reg_num) + "\r\n")
##                            buf = []
##                            for i in self.recv_buffer:
##                                buf.append(hex(i))
##                            print(str(buf) + '\r\n')
                            if self.m_or_s == "master":
                                #print("master\r\n")
                                if func == 0x00:#回复寄存器
##                                    print(str(reg_num*6+5) + ":" + str(len(self.recv_buffer)))
                                    if reg_num*6 + 5 == len(self.recv_buffer):
                                        self.prot.decode(self.recv_time, self.recv_buffer)
                                        #print("\r\n")
                                        self.recv_buffer.clear() #清空buffer
                                elif func == 0x40:#回复状态信息
##                                    print(str(reg_num+7) + ":" + str(len(self.recv_buffer)))
                                    if reg_num + 7 == len(self.recv_buffer):
                                       #print('\033[32m Master ')
                                        #print('\033[32m Master ' + self.recv_time)
##                                        buf = []
##                                        for i in self.recv_buffer:
##                                            buf.append(hex(i))
##                                        print(str(buf) + "\r\n\r\n")
                                        self.prot.decode(self.recv_time, self.recv_buffer)
                                        #print("\r\n")
                                        self.recv_buffer.clear() #清空buffer
                            elif self.m_or_s == "slave":
##                                print("slave\r\n")
                                if func == 0x00:#设置寄存器
                                    if reg_num*6 + 5 == len(self.recv_buffer):
                                        #print("\033[35mSlave " + self.recv_time)
##                                        buf = []
##                                        for i in self.recv_buffer:
##                                            buf.append(hex(i))
##                                        print(str(buf) + "\r\n\r\n")
                                        self.prot.decode(self.recv_time, self.recv_buffer)
                                        #print("\r\n")
                                        self.recv_buffer.clear() #清空buffer
                                elif func == 0x40:#读寄存器
                                    if reg_num*2 + 5 == len(self.recv_buffer):
                                        #print("\033[35mSlave " + self.recv_time)
##                                        buf = []
##                                        for i in self.recv_buffer:
##                                            buf.append(hex(i))
##                                        print(str(buf) + "\r\n\r\n")
                                        self.prot.decode(self.recv_time, self.recv_buffer)
##                                        print("\r\n")
                                        self.recv_buffer.clear() #清空buffer


                        if len(self.recv_buffer) > 101:
                            self.recv_buffer.clear() #清空buffer
                    
                time.sleep(0.001)
        except BaseException as e:
            self.close()
            print("recv_task_func err：",e)
                    
            

if '__main__' == __name__:
    
    dat = [1,2,3,4,5,6,7,8]
    ser = SerialCom("COM10")
    #ser.open()
    #ser.send(dat)
    #ser.close()
