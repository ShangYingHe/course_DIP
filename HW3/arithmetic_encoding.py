# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 14:28:13 2018

@author: sun
"""

import numpy as np
from matplotlib import pyplot as plt
import math

class Codeword:
    def __init__(self):
        self.lower = 0.0
        self.upper = 1.0
    def diff(self):
        return self.upper - self.lower
def to_symbol(image,num_per_symbol):
    symbols = np.concatenate(np.split(image,image.shape[1]/num_per_symbol,axis=1),axis=0)
    symbol_list = np.unique(symbols,axis=0)
    hist = np.histogramdd(symbols,bins=symbol_list.shape[0])[0]
    a = hist[np.nonzero(hist)]
    prob = a/np.sum(a)
    return symbols,symbol_list.tolist(),prob
def ar_encoding_symbol(image):
    symbols,symbol_list,prob = to_symbol(image,2)
    codeword = []
    cdf = np.insert(np.cumsum(prob),0,0.0)
    code = Codeword()
    k = 1
    for i in symbols:
        ind = symbol_list.index(i.tolist())        
        l = (code.diff()*cdf[ind])+code.lower
        u = (code.diff()*cdf[ind+1])+code.lower
        code.lower = l
        code.upper = u       
        if k%4==0:
            codeword.append((code.lower+code.upper)/2)
            code.__init__()
        k+=1
    return codeword
def ar_encoding(image):
    codeword = []
    N = 4
    hist = np.bincount(image.flatten(),minlength=256).astype('float32')
    prob = hist/np.sum(hist)
    cdf = np.cumsum(prob)
    code = Codeword()
    k = 1
    for i in image.flatten():
        l = (code.diff()*cdf[i])+code.lower
        u = (code.diff()*cdf[i+1])+code.lower
        code.lower = l
        code.upper = u       
        if k%N==0:
            codeword.append(round((code.lower+code.upper)/2,8))
            code.__init__()
        k+=1
    f = open('./result/arithmetic_codes.txt','w')
    for code in codeword:
        f.write(str(code)+'\n')
    f.close
    bit_per_word = math.ceil(math.log2(99999999))
    compression_ratio = 8/(len(codeword)*bit_per_word/image.size)
    return compression_ratio,codeword

if __name__ == '__main__':
    image = plt.imread('./data/image2.bmp')
    compression_ratio,codeword = ar_encoding(image)
    print(compression_ratio)
#    symbols,symbol_list,prob = to_symbol(image,2)
#    test = np.array([1,3,2,1,1,1,1,1,1,1,
#                     1,1,1,1,1,1,1,1,1,1,
#                     1,1,1,1,1,1,1,1,1,1,
#                     1,1,1,1,1,1,1,1,1,1,
#                     1,1,1,1,1,1,1,1,1,1,
#                     1,1,1,1,1,1,1,1,1,1,
#                     1,1,1,1,1,1,1,1,1,1,
#                     1,1,1,1,1,1,1,1,1,1,
#                     1,2,
#                     1,3,3,3,3,3,3,3,3,3,
#                     3,3,3,3,3,3,3,3,])
#    ar_encoding(test)