# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 01:18:48 2018

@author: sun
"""

from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from scipy import fftpack
import numpy as np
import math

def D(u,v,u0,v0):
    return (((u-u0)**2)+((v-v0)**2))**(1/2)
def ideal_bandreject(array,w,C0):
    H = np.ones(array.shape)
    u0 = array.shape[0]//2
    v0 = array.shape[1]//2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if (C0-(w/2))<=D(i,j,u0,v0)<=(C0+(w/2)):
                H[i,j] = 0
    return H
def butterworth_bandreject(array,w,C0,n):
    H = np.ones(array.shape)
    u0 = array.shape[0]/2
    v0 = array.shape[1]/2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):          
            H[i,j] = 1/(1+((D(i,j,u0,v0)*w)/(D(i,j,u0,v0)**2-C0**2))**(2*n))
    return H
def gaussian_bandreject(array,w,C0):
    H = np.ones(array.shape)
    u0 = array.shape[0]/2
    v0 = array.shape[1]/2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):          
            H[i,j] = 1-math.exp(-((D(i,j,u0,v0)**2-C0**2)/(D(i,j,u0,v0)*w))**2)
    return H


image = mpimg.imread(r'D:\影像處理\HW2\test images\3.png')

fourier_image = np.fft.fft2(image)
fourier_image = fftpack.fftshift(fourier_image)

point1 = np.argwhere(fourier_image == np.amax(fourier_image[:,100:300]))
point2 = np.argwhere(fourier_image == np.amax(fourier_image[:,700:900]))

H = gaussian_bandreject(fourier_image,60,300)

filtered_image = fourier_image*H

result = fftpack.ifftshift(filtered_image)
result = np.real(np.fft.ifft2(result))

plt.figure(0)
plt.imshow(image,cmap='gray')
plt.figure(1)
plt.imshow(np.log10(np.abs(fourier_image)),cmap='gray')
plt.figure(2)
plt.imshow(H,cmap='gray')

plt.figure(3)
plt.imshow(np.log10(np.abs(filtered_image)),cmap='gray')
plt.figure(4)
plt.imshow(result,cmap='gray')

#plt.imsave(r'D:\影像處理\HW2\3_fourier.png',np.log10(np.abs(fourier_image)),cmap='gray')
#plt.imsave(r'D:\影像處理\HW2\3_filter.png',H,cmap='gray')
#plt.imsave(r'D:\影像處理\HW2\3_filtered.png',result,cmap='gray')