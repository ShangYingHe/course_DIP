# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 23:49:15 2018

@author: sun
"""

from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from scipy import fftpack
import numpy as np
import math
from skimage import exposure

def D(u,v,u0,v0):
    return (((u-u0)**2)+((v-v0)**2))**(1/2)
def ideal_high_pass(array,D0):
    H = np.ones(array.shape)
    u0 = array.shape[0]//2
    v0 = array.shape[1]//2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if D(i,j,u0,v0) <= D0:
                H[i,j] = 0
    return H
def butterworth_high_pass(array,D0,n):
    H = np.ones(array.shape)
    u0 = array.shape[0]/2
    v0 = array.shape[1]/2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            H[i,j] = 1/(1+(D(i,j,u0,v0)/D0)**(2*n))
    return 1-H
def gaussian_high_pass(array,D0):
    H = np.ones(array.shape)
    u0 = array.shape[0]/2
    v0 = array.shape[1]/2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            H[i,j] = 1-math.exp(-(D(i,j,u0,v0)**2)/(2*(D0**2)))
    return H

image = mpimg.imread(r'D:\影像處理\HW2\test images\original.jpg')
#image1 = mpimg.imread(r'D:\影像處理\HW2\test.jpg')/255

t = np.log1p(image)

fourier_image = np.fft.fft2(t)
fourier_image = fftpack.fftshift(fourier_image)

point1 = np.argwhere(fourier_image == np.amax(fourier_image[:,100:300]))
point2 = np.argwhere(fourier_image == np.amax(fourier_image[:,700:900]))

#H = ideal_high_pass(fourier_image,30)
H = butterworth_high_pass(fourier_image,30,2)
#H = gaussian_high_pass(fourier_image,30)


filtered_image = fourier_image*(0.75 + 1.25*H)

result = fftpack.ifftshift(filtered_image)
result = np.exp(np.real(np.fft.ifft2(result)))-1

#result = image+image1[:,:,0]

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
plt.imsave(r'D:\影像處理\HW2\test.jpg',result,cmap='gray')