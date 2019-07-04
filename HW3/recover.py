# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 23:44:52 2018

@author: sun
"""

import numpy as np
from matplotlib import pyplot as plt

def correlation_score(CorrCoeMatirx):
    target = np.ones_like(CorrCoeMatirx)
    score = abs(np.sum(target-np.abs(CorrCoeMatirx)))
    return score
def recover(shifted_image,mode):
    image = shifted_image.copy()
    a=[]
    if mode == 'row':
        for i in range(image.shape[0]-1):
            for j in range(image.shape[1]):
                a.append(correlation_score(np.corrcoef(image[i,:],np.roll(image[i+1,:],j,axis=0))))
            image[i+1,:] = np.roll(image[i+1,:],np.argmin(np.asarray(a)),axis=0)
            a.clear()
    elif mode == 'col':
        for i in range(image.shape[1]-1):
            for j in range(image.shape[0]):
                a.append(correlation_score(np.corrcoef(image[:,i],np.roll(image[:,i+1],j,axis=0))))
            image[:,i+1] = np.roll(image[:,i+1],np.argmin(np.asarray(a)),axis=0)
            a.clear()
    return image
def recover_row(shifted_image):
    image = shifted_image.copy()
    a=[]
    for i in range(image.shape[0]-1):
        for j in range(image.shape[1]):
            a.append(correlation_score(np.corrcoef(image[i,:],np.roll(image[i+1,:],j,axis=0))))
        image[i+1,:] = np.roll(image[i+1,:],np.argmin(np.asarray(a)),axis=0)
        a.clear()
    return image
def recover_col(shifted_image):
    image = shifted_image.copy()
    a=[]
    for i in range(image.shape[1]-1):
        for j in range(image.shape[0]):
            a.append(correlation_score(np.corrcoef(image[:,i],np.roll(image[:,i+1],j,axis=0))))
        image[:,i+1] = np.roll(image[:,i+1],np.argmin(np.asarray(a)),axis=0)
        a.clear()
    return image
if __name__ == '__main__':
    image = plt.imread('./data/image3.bmp')
    recover_image = recover(image,mode='row')
    plt.imsave('./3_recover.jpg',recover_image,cmap='gray')
    plt.imshow(recover_image,cmap='gray')
    plt.show()