#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: ChengBingBing

from ComProtocol import ComMaster, ComSlave, ComProtocol
from Debug import Debug
from Debug import DEBUG_MOD
import time,threading
from SerialCom import SerialCom
import datetime


class Main:
    
    def __init__(self, m_com, s_com, m_baud=115200, s_baud=115200):
        debug = Debug()
        self.m_com = m_com
        self.s_com = s_com
        if m_com != "DISABLE":
            self.master_com = SerialCom(m_com,"master",m_baud)

        if s_com != "DISABLE":
            self.slave_com = SerialCom(s_com,"slave",s_baud)
        
        #创建接收任务
        self.main_task = threading.Thread(target=self.main_task_func, name='main task thread')
        self.main_task.start()   
    
    def main_task_func(self):
##        while True:
##            if self.m_com != "DISABLE":
##                if len(self.master_com.recv_buffer_list) != 0:
##                    buffer = self.master_com.recv_buffer_list.pop(0)
##                    recv_time = self.master_com.recv_time.pop(0)
##                    print("Master time: ", recv_time)
##                    self.master_port.deocde(buffer)
##                    
##            if self.s_com != "DISABLE":
##                if len(self.slave_com.recv_buffer_list) != 0:
##                    buffer = self.slave_com.recv_buffer_list.pop(0)
##                    recv_time = self.slave_com.recv_time.pop(0)
##                    print("Slave, time: ", recv_time)
##                    self.slave_port.deocde(buffer)

            time.sleep(0.01)
    


if '__main__' == __name__:
    #main = Main("COM10", "COM11")
    main = Main("COM10", "COM11")
    
    #debug_task = threading.Thread(target=debug_task_func, name='debug task thread')
    #debug_task.start()
    
