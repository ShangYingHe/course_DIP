# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 16:45:29 2018

@author: sun
"""

from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from scipy import fftpack
import numpy as np
import math
import cmath

def D(u,v,u0,v0):                   #euclidean distance
    return (((u-u0)**2)+((v-v0)**2))**(1/2)
def degradation_H(array,k):         #degradation function for 1.jpg
    H = np.zeros(array.shape)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            u = i-array.shape[0]/2
            v = j-array.shape[1]/2
            H[i,j] = math.exp(-k*((u**2+v**2)**(5/6)))
    return H
def degradation_motion_H(array,a,b,t):#degradation function for 2.jpg
    H = np.zeros(array.shape,dtype=complex)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            u=i-array.shape[0]/2
            v=j-array.shape[1]/2
            if (u*a)+(v*b)==0:
                H[i,j]=1
            else:
                C1=(t/(math.pi*((u*a)+(v*b))))
                C2=math.sin(math.pi*((u*a)+(v*b)))
                C3=cmath.exp(-1j*(math.pi*((u*a)+(v*b))))
                H[i,j] = C1*C2*C3            
    return H
def my_H(array):
    H = np.ones(array.shape)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if round(0.6*j+20.356)==i or round(0.6*j+151.683)==i:
                H[i:i+20,j:j+30]=10
    return H
def wiener(H,K):                       #wiener filter function
    H = (1/H)*((np.abs(H)**2)/(np.abs(H)**2+K))
    return H
def shift(array):
    a = np.zeros(array.shape)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            a[i,j]=array[i-array.shape[0]//2,j-array.shape[1]//2]
    return a

image = mpimg.imread('./test images/2.jpg')

fourier_image = np.fft.fft2(image)  #fourier transform
fourier_image = fftpack.fftshift(fourier_image) #move low frequency to middle

point1 = np.argwhere(fourier_image == np.amax(fourier_image[200:300,100:200]))
point2 = np.argwhere(fourier_image == np.amax(fourier_image[300:400,300:400]))
point3 = np.argwhere(fourier_image == np.amax(fourier_image[100:200,100:200]))
point4 = np.argwhere(fourier_image == np.amax(fourier_image[200:300,300:400]))

#H = wiener(degradation_motion_H(fourier_image,0.018,-0.012,3),0.0001)
degradation = degradation_motion_H(fourier_image,0.0155,-0.0105,0.5)    #perform degradation
H = wiener(degradation,0.01)    #perform wiener filter
filtered_image = H*fourier_image #filtering

result = fftpack.ifftshift(filtered_image)  #move frequency from middle back
result = np.real(np.fft.ifft2(result))      #inverse fourier transform

plt.figure(0)
plt.imshow(image,cmap='gray')
plt.figure(1)
plt.imshow(np.log10(np.abs(fourier_image)),cmap='gray')
plt.figure(2)
plt.imshow((np.abs(H)**(1/4)),cmap='gray')

plt.figure(3)
plt.imshow(np.log10(np.abs(filtered_image)),cmap='gray')
plt.figure(4)
plt.imshow(result,cmap='gray')

#plt.imsave(r'D:\影像處理\HW2\2_fourier.png',np.log10(np.abs(fourier_image)),cmap='gray')
#plt.imsave(r'D:\影像處理\HW2\2_filtered.png',result,cmap='gray')