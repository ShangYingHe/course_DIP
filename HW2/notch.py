# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 23:50:59 2018

@author: sun
"""

from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from scipy import fftpack
import numpy as np

def D(u,v,M,N):
    D = (((u-M)/(2))**2 + ((v-N)/(2))**2)**(1/2)

    return D
def filter_H(array,p1,p2,D0):
    H = np.ones(array.shape)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            D1 = D(i,j,p1[0,0],p1[0,1])
            D2 = D(i,j,p2[0,0],p2[0,1])
            if D1<=D0 or D2<=D0:
                H[i,j] = 0
    return H

image = mpimg.imread(r'D:\影像處理\HW2\test images\4.png')

fourier_image = np.fft.fft2(image)
fourier_image = fftpack.fftshift(fourier_image)
print(np.max(fourier_image))

point1 = np.argwhere(fourier_image == np.amax(fourier_image[280:360,280:360]))
point2 = np.argwhere(fourier_image == np.amax(fourier_image[680:760,680:760]))
H = filter_H(fourier_image,point1,point2,10)

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

#plt.imsave(r'D:\影像處理\HW2\4_fourier.png',np.log10(np.abs(fourier_image)),cmap='gray')
#plt.imsave(r'D:\影像處理\HW2\4_filter.png',H,cmap='gray')
#plt.imsave(r'D:\影像處理\HW2\4_filtered.png',result,cmap='gray')