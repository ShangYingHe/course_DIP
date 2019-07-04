# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 00:33:12 2018

@author: sun
"""

import numpy as np
from matplotlib import pyplot as plt
import time

def entropy(image):
    hist = np.bincount(image.flatten(),minlength=256)
    pb = hist/np.sum(hist)
    pb_del_zero = np.delete(pb,np.argwhere(pb==0))
    return -np.sum(pb_del_zero*np.log2(pb_del_zero))
def horizontal_entropy(image_array):
    l = []
    for i in range(image_array.shape[1]):
        c = np.concatenate((image_array[:,i].reshape(image_array.shape[0],1),np.roll(image_array,-1)[:,i].reshape(image_array.shape[0],1)),axis=1)
        for j in range(c.shape[0]):
            l.append(c[j,:].tolist())
    l_remove_repeat = []
    count = []
    for i in l:
        if not i in l_remove_repeat:
            l_remove_repeat.append(i)
    for i in l_remove_repeat:
        count.append(l.count(i))
    pb = np.asarray(count)/len(l)
    return -np.sum(pb*np.log2(pb))/2
def horizontal_entropy_fast(image):
    col0 = image[:,0].reshape(image.shape[0],1)
    image_extend = np.concatenate((col0,np.repeat(image[:,1:],2,axis=1),col0),axis=1)
    pair = np.concatenate(np.split(image_extend,image.shape[1],axis=1),axis=0)
#    print(np.unique(pair,axis=0))
    hist = np.histogramdd(pair,bins=np.unique(pair,axis=0).shape[0])[0]
    a = hist[np.nonzero(hist)]
    pb = a/np.sum(a)
    return -np.sum(pb*np.log2(pb))/2

if __name__ == '__main__':
    image = plt.imread('./data/image2.bmp')
    entropy = entropy(image)
    print(entropy)
    
#    atstart = time.time()
#    a = horizontal_entropy(image)
#    aend = time.time()
#    print('horizontal_entropy cost %f sec\n'%(aend-atstart),'entropy is %f'%a)
    
#    btstart = time.time()
#    b = horizontal_entropy_fast(image)
#    bend = time.time()
#    print('horizontal_entropy_fast cost %f sec\n'%(bend-btstart),'entropy is %f'%b)