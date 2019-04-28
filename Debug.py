#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: ChengBingBing

from enum import Enum
import threading
import time

class DEBUG_MOD(Enum):
    NONE = 0,
    PROTOCOL = 1,
    CONFIG = 2

class Debug:
    trace_str = []
    trace_mod = []
    _instance_lock = threading.Lock()
   
    def __init__(self):
        #创建接收任务
        self.debug_task = threading.Thread(target=self.debug_task_func, name='debug task thread')
        self.debug_task.start()    

    #单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(Debug, "_instance"):
            with Debug._instance_lock:
                if not hasattr(Debug, "_instance"):
                    Debug._instance = object.__new__(cls)  
        return Debug._instance

    #使能模块打印
    def module_en(self, module):
        for i in self.trace_mod:
            if i == module:
                return

        self.trace_mod.append(module)
        

    #禁用模块打印
    def module_dis(self, module):
        index = 0
        for i in self.trace_mod:
            if i == module:
                self.trace_mod.pop(index)
            index += 1

    #调试追踪
    def trace(self, module, string):
        for i in self.trace_mod:
            if i == module: #搜索
                if module == DEBUG_MOD.NONE:
                    return;
                elif module == DEBUG_MOD.PROTOCOL:
                    self.trace_str.append('[PROTOCOL] ' + string + '\r')
                elif module == DEBUG_MOD.CONFIG:
                    self.trace_str.append('[CONFIG] ' + string + '\r')


    #调试数据输出
    def output(self):
        if self.trace_str:
            string = self.trace_str.pop(0)
            if string:
                print(string)

    def debug_task_func(self):
        while True:
            self.output();
            time.sleep(0.01)


if '__main__' == __name__:
    debug = Debug()
    debug1 = Debug()
    
    debug.module_en(DEBUG_MOD.CONFIG)
    debug.module_en(DEBUG_MOD.PROTOCOL)
    
    debug.trace(DEBUG_MOD.CONFIG, '123')
    debug1.trace(DEBUG_MOD.CONFIG, "213")
    debug.trace(DEBUG_MOD.CONFIG,"312")
    debug1.output();
    debug.output();
    debug.output();
    debug.output();
    debug.output();
    debug.output();
