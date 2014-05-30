#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
import traceback

HEADER_LEN = 8
FILTER_LEN = 3
PARTITION_LEN = 3
SERIAL_LEN = 38
JCP_SERIAL_LEN = 35 # for jcp
PARTITION_PREFIX_NBR = {
    0:[40,4],
    1:[37,7],
    2:[34,10],
    3:[30,14],
    4:[27,17],
    5:[24,20],
    6:[20,24],
}
class convertpy:
    def __init__(self):
        #self.string_num = string_num
        #base = [0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F]
        self.base = [str(x) for x in range(10)] + [chr(x) for x in range(ord('A'),ord('A')+6)]

    #2 to 10
    def bin2dec(self,string_num):
        return str(int(string_num,2))

    #16 to 10
    def hex2dec(self,string_num):
        try:
            decNum =  str(int(string_num.upper(),16))
            return decNum
        except:
            raise

    #10 to 2
    def dec2bin(self,string_num,length=0):
        num = int(string_num)
        mid = []
        while True:
            if num == 0: break
            num,rem = divmod(num,2)
            mid.append(self.base[rem])
        value = ''.join([str(x) for x in mid[::-1]])
        if length == 0:
            return value
        else:
            rest_len = length - len(value)
            value = '0'*rest_len + value
            return value

    #10 to 16
    def dec2hex(self,string_num):
        num = int(string_num)
        mid = []
        while True:
            if num == 0: break
            num,rem = divmod(num,16)
            mid.append(self.base[rem])
        return ''.join([str(x) for x in mid[::-1]])

    #16 to 2
    def hex2bin(self,string_num):
        return self.dec2bin(self.hex2dec(string_num.upper()))

    #2 to 16
    def bin2hex(self,string_num):
        return self.dec2hex(self.bin2dec(string_num))

class upcToepc:
    def __init__(self):
        pass

    def run(self,begin,upc,qty,header=48,fitler=1,partition=5):
        try:
            obj = convertpy()
            rs = []
            for i in range(begin,qty+begin):
                string_num = obj.dec2bin(header,HEADER_LEN)
                string_num += obj.dec2bin(fitler,FILTER_LEN)
                string_num += obj.dec2bin(partition,PARTITION_LEN)               
                upcA = "0" + upc[:6] if len(upc) == 12 else upc[0:7]
                upcB = "0" + upc[6:-1] if len(upc) == 12 else upc[7:-1]
                string_num += obj.dec2bin(upcA,PARTITION_PREFIX_NBR[partition][0])
                string_num += obj.dec2bin(upcB,PARTITION_PREFIX_NBR[partition][1])
#                string_num += obj.dec2bin(i,SERIAL_LEN)
                string_num += "110" + obj.dec2bin(i, JCP_SERIAL_LEN) # for jcp
                value = obj.bin2hex(string_num)
                rs.append(value)
            return rs
        except:
            traceback.print_exc()



if __name__ == "__main__":
    try:
        obj = upcToepc()

        upc = ['075338723709']
        #8000000001
        for u in upc:
            data  = obj.run(6995,u,1)
            print data
        #map(obj.run,upc*20,[i for i in range(0,20)])

        '''
        for i in range(0,20):
            obj.run(48,1,5,upc,i)
        string_num = '00110000  001  101  000000010011001110010110  00001011010001010101  00000001001001100101100000001011010010'
        obj = convertpy()
        string_num = string_num.replace(' ','')
        value = obj.bin2hex(string_num)
        print value

        #10 to 2
        string_num = '78742'
        value = obj.dec2bin(string_num,24)
        print value
        '''
    except:
        traceback.print_exc()
