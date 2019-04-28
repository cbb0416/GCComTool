#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: ChengBingBing



from Debug import Debug
from Debug import DEBUG_MOD
from enum import Enum
from Filter import Filter

FRAME_TAIL = 0xC3

aucCRCHi = [
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40]

aucCRCLo = [
0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06, 0x07, 0xC7,
0x05, 0xC5, 0xC4, 0x04, 0xCC, 0x0C, 0x0D, 0xCD, 0x0F, 0xCF, 0xCE, 0x0E,
0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09, 0x08, 0xC8, 0xD8, 0x18, 0x19, 0xD9,
0x1B, 0xDB, 0xDA, 0x1A, 0x1E, 0xDE, 0xDF, 0x1F, 0xDD, 0x1D, 0x1C, 0xDC,
0x14, 0xD4, 0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3,
0x11, 0xD1, 0xD0, 0x10, 0xF0, 0x30, 0x31, 0xF1, 0x33, 0xF3, 0xF2, 0x32,
0x36, 0xF6, 0xF7, 0x37, 0xF5, 0x35, 0x34, 0xF4, 0x3C, 0xFC, 0xFD, 0x3D,
0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A, 0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38,
0x28, 0xE8, 0xE9, 0x29, 0xEB, 0x2B, 0x2A, 0xEA, 0xEE, 0x2E, 0x2F, 0xEF,
0x2D, 0xED, 0xEC, 0x2C, 0xE4, 0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26,
0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0, 0xA0, 0x60, 0x61, 0xA1,
0x63, 0xA3, 0xA2, 0x62, 0x66, 0xA6, 0xA7, 0x67, 0xA5, 0x65, 0x64, 0xA4,
0x6C, 0xAC, 0xAD, 0x6D, 0xAF, 0x6F, 0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB,
0x69, 0xA9, 0xA8, 0x68, 0x78, 0xB8, 0xB9, 0x79, 0xBB, 0x7B, 0x7A, 0xBA,
0xBE, 0x7E, 0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C, 0xB4, 0x74, 0x75, 0xB5,
0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71, 0x70, 0xB0,
0x50, 0x90, 0x91, 0x51, 0x93, 0x53, 0x52, 0x92, 0x96, 0x56, 0x57, 0x97,
0x55, 0x95, 0x94, 0x54, 0x9C, 0x5C, 0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E,
0x5A, 0x9A, 0x9B, 0x5B, 0x99, 0x59, 0x58, 0x98, 0x88, 0x48, 0x49, 0x89,
0x4B, 0x8B, 0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C,
0x44, 0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42, 0x43, 0x83,
0x41, 0x81, 0x80, 0x40]

class PROT_FUNC(Enum):
    NONE = 0,
    SET_REG = 1,
    SET_STR = 2,
    GET_REG = 3,
    RESP_REG = 4,
    RESP_STATE = 5

class ComProtocol(object):
    reg_id = []
    reg_value = []
    reg_num = 0
    func = PROT_FUNC
    resp_state = 0
    resp_frame_err = 0
    resp_set_reg_err = []
    transmit_dat = []
    dbg = Debug()
	
    def __init__(self):
        self.filter = Filter()
            
    def crc_generate(self, dat):
        crc_hi = 0xFF
        crc_lo = 0xFF
        index = 0

        for i in dat:
            index = crc_lo ^ i
            crc_lo = crc_hi ^ aucCRCHi[index]
            crc_hi = aucCRCLo[index]

        return crc_hi <<8 | crc_lo

    def crc_check(self, dat, crc):
        crc_ret = self.crc_generate(dat)
        if crc_ret == crc:
            self.debug('crc check success')
            return True
        else:
            self.debug('crc check failed')
            return False

    def frame_check(self, dat, head):
        #帧长度判断
        if (len(dat) <= 7) or (len(dat) > 101):
            self.debug('Frame Len Error')
            return False
        
        #帧头判断
        if dat[0] != head:
            self.debug('Frame Head Error')
            return False
        
        #帧尾判断
        if dat[-1] != FRAME_TAIL:
            self.debug('Frame Tail Error')
            return False

        #CRC校验
        crc = dat[-2] << 8 | dat[-3] #提取数据中的CRC值
        crc_dat = dat[1:-3]   #提取参与CRC校验的数据
        return self.crc_check(crc_dat, crc)

    def debug(self, string):
        self.dbg.trace(DEBUG_MOD.PROTOCOL, string)

    def debug_en(self):
        self.dbg.module_en(DEBUG_MOD.PROTOCOL)

    def debug_dis(self):
        self.dbg.module_dis(DEBUG_MOD.PROTOCOL)

#主机（底板或电脑）
class ComMaster(ComProtocol):
    
    def get_frame_func(self, byte):
        fc = byte & 0x70
        if fc == 0:
            self.debug('func: resp reg')
            return PROT_FUNC.RESP_REG
        elif fc == 0x40:
            self.debug('func: resp state')
            return PROT_FUNC.RESP_STATE
        else:
            self.debug('func: error')
            return PROT_FUNC.NONE

    #根据功能码及寄存器数量计算帧长度
    #func: 功能码
    #reg_num: 寄存器数量
    def calc_frame_len(self, func, reg_num):
        if func == PROT_FUNC.RESP_REG:
            return (5 +reg_num*6)
        elif func == PROT_FUNC.RESP_STATE:
            return (7+ reg_num)
        else:
            return 0

    #获取回复值
    def get_frame_reg(self, time, dat):
        if self.func == PROT_FUNC.RESP_REG:
            for i in range(self.reg_num):
                self.reg_id.append((dat[2 + i*6] << 8) | dat[3 + i*6])
                self.reg_value.append((dat[4 + i*6] << 24) | (dat[5 + i*6] << 16) | (dat[6 + i*6] << 8) | dat[7 + i*6])
                #self.debug("RESP ID: " + str(self.reg_id[i]) + " VALUE: "+ str(self.reg_value[i]))
                #print("RESP ID: " + str(self.reg_id[i]) + " VALUE: "+ str(self.reg_value[i]))
            self.filter.recv_filter(time, "RESP_REG", self.reg_id, self.reg_value)
            # 清空
            self.reg_id.clear()
            self.reg_value.clear()

        elif self.func == PROT_FUNC.RESP_STATE:
            self.resp_state = dat[2]
            #self.debug("RESP STATE: " + str(self.resp_state))
            #print("RESP STATE: " + str(self.resp_state))
            self.resp_frame_err = dat[3]
            #self.debug("RESP FRAME ERR: " + str(self.resp_frame_err))
            #print("RESP FRAME ERR: " + str(self.resp_frame_err))
            resp_reg_err = []
            for i in range(self.reg_num):
                self.resp_set_reg_err.append(dat[4+i])
                #self.debug("RESP SET REG ERR: " + str(self.resp_set_reg_err[i]))
                resp_reg_err.append(self.resp_set_reg_err[i])
            #self.debug("RESP STATE: " + str(self.resp_state) + " RESP FRAME ERR: " + str(self.resp_frame_err) + " RESP SET REG ERR: " + str(reg_err))
            #print("RESP STATE: " + str(self.resp_state) + " RESP FRAME ERR: " + str(self.resp_frame_err) + " RESP SET REG ERR: " + str(reg_err))
            self.filter.recv_filter(time, "RESP_STATE", state=self.resp_state, frame_err=self.resp_frame_err, reg_err = resp_reg_err)
            
    def decode(self, time, dat):
        frame_len = 0

        #CRC校验
        if self.frame_check(dat, 0x5A) == True:
            self.debug('frame check success')
        else:
            self.debug('frame check failed')
            return False

        self.func = self.get_frame_func(dat[1])
        self.reg_num = dat[1] & 0x0F
        self.reg_num += 1
        self.debug('reg num:' + str(self.reg_num))

        #实际数据长度与理论帧长度不一致
        if self.calc_frame_len(self.func, self.reg_num) != len(dat):
            self.debug(str(self.calc_frame_len(self.func, self.reg_num, dat[2])))
            self.debug(str(len(dat)))
            self.debug('frame length is notequal length of dat!')
            return False

        #寄存器提取
        self.get_frame_reg(time, dat)

        return True

#从机（核心板）
class ComSlave(ComProtocol):
    def get_frame_func(self, byte):
        fc = byte & 0x70
        if fc == 0:
            self.debug('func: set reg')
            return PROT_FUNC.SET_REG
        elif fc == 0x10:
            self.debug('func: set string')
            return PROT_FUNC.SET_STR
        elif fc == 0x40:
            self.debug('func: get reg')
            return PROT_FUNC.GET_REG
        else:
            self.debug('func: error')
            return PROT_FUNC.NONE

    #根据功能码及寄存器数量计算帧长度
    #func: 功能码
    #reg_num: 寄存器数量
    #set_str_len: 设置字符串寄存器帧中命令总长度
    def calc_frame_len(self, func, reg_num, set_str_len):
        if func == PROT_FUNC.SET_REG:
            return (5 +reg_num*6)
        elif func == PROT_FUNC.SET_STR:
            return (6 + dat[2])
        elif func == PROT_FUNC.GET_REG:
            return (5 + reg_num*2)
        else:
            return 0

    #获取寄存器ID和数值
    def get_frame_reg(self, time, dat):
        if self.func == PROT_FUNC.SET_REG:
            self.debug('range(reg_num): ' + str(range(self.reg_num)))
            for i in range(self.reg_num):
                self.reg_id.append((dat[2 + i*6] << 8) | dat[3 + i*6])
                self.reg_value.append((dat[4 + i*6] << 24) | (dat[5 + i*6] << 16) | (dat[6 + i*6] << 8) | dat[7 + i*6])
                #self.debug("ID: " + str(self.reg_id[i]) + " VALUE: "+ str(self.reg_value[i]))
                #print("ID: " + str(self.reg_id[i]) + " VALUE: "+ str(self.reg_value[i]))
            self.filter.recv_filter(time, "SET_REG", self.reg_id, self.reg_value)
            # 清空
            self.reg_id.clear()
            self.reg_value.clear()

        elif self.func == PROT_FUNC.SET_STR:
            # 清空
            self.reg_id.clear()
            self.reg_value.clear()
            pass
        elif self.func == PROT_FUNC.GET_REG:
            for i in range(self.reg_num):
                self.reg_id.append((dat[2 + i*2] << 8) | dat[3 + i*2])
                #self.debug("ID: " + str(self.reg_id[i]))
                #print("ID: " + str(self.reg_id[i]))
            self.filter.recv_filter(time, "GET_REG", self.reg_id)
            # 清空
            self.reg_id.clear()
            self.reg_value.clear()

    def decode(self, time, dat):
        frame_len = 0

        #CRC校验
        if self.frame_check(dat, 0xA5) == True:
            self.debug('frame check success')
        else:
            self.debug('frame check failed')
            return False

        self.func = self.get_frame_func(dat[1])
        self.reg_num = dat[1] & 0x0F
        self.reg_num += 1
        self.debug('reg num:' + str(self.reg_num))

        #实际数据长度与理论帧长度不一致
        if self.calc_frame_len(self.func, self.reg_num, dat[2]) != len(dat):
            self.debug(str(self.calc_frame_len(self.func, self.reg_num, dat[2])))
            self.debug(str(len(dat)))
            self.debug('frame length is notequal length of dat!')
            return False

        #寄存器提取
        self.get_frame_reg(time, dat)

        return True

if '__main__' == __name__:
    dat = [0xA5, 0x80, 0x00, 0x02, 0x00, 0x00, 0x00, 0x04, 0xE2, 0xCB, 0xC3 ]

    master = ComMaster()
    master.debug_en()
    master.decode(dat)
    
