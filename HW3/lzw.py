# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 01:31:17 2018

@author: sun
"""

import numpy as np
from matplotlib import pyplot as plt
import string
import math
import json

def test():
    data = 'tobeornottobeortobeornot'
    dictnary = dict.fromkeys(string.ascii_lowercase[:26])
    n = 1
    for i in dictnary:
        dictnary[i] = n
        n+=1
    return data,dictnary
def inidict():
    a = dict()
    for i in range(256):
        a[str(i)] = i
    return a
def lzw_encoding(data,dictnary):
    codeword = []
    k=0
    while k < len(data)-1:
        current = data[k]
        nex = data[k+1]
        seq = [current,nex]       
        while str(seq) in dictnary and nex != None:        
            current = seq.copy()
            k+=1
            try:
                nex = data[k+1]
                seq.append(nex)
            except:
                nex = None
        if nex != None:
#            print(current,nex,dictnary[str(current)],str(seq),len(dictnary)+1)
            dictnary[str(seq)] = len(dictnary)      # +1 if test
            codeword.append(dictnary[str(current)])
            k+=1
        else:
            codeword.append(dictnary[str(current)])
    f = open('./result/lzw_codes.txt','w')
    for code in codeword:
        f.write(str(code)+'\n')
    f.close
    f = open('./result/lzw_dictnary.txt','w')
    f.write(json.dumps(dictnary))
    f.close
    return codeword,dictnary
        
if __name__ == '__main__':
    image = plt.imread('./data/image2.bmp')
    codeword,dictnary = lzw_encoding(image.flatten(),inidict())
    print(math.log2(len(dictnary)))
    bit_per_word = math.ceil(math.log2(len(dictnary)))
    compression_ratio = 8/(len(codeword)*bit_per_word/len(image.flatten()))
    print(compression_ratio)
    hist = np.bincount(image.flatten(),minlength=256)
#-------------------test--------------------
#    data,dictnary = test()
#    codeword,dictnary = lzw_encoding(data,dictnary)
#    print(codeword)