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

if '__main__' == __name__:
    #main = Main("COM10", "COM11")
    main = Main("COM10", "COM11")
    
    #debug_task = threading.Thread(target=debug_task_func, name='debug task thread')
    #debug_task.start()
    
