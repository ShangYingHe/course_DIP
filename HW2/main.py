# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 19:09:19 2018

@author: sun
"""

import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from tkinter import filedialog
from PIL import Image, ImageTk
from skimage.transform import resize
from scipy import misc
from scipy import fftpack
import math
import cmath
from matplotlib import colors

def show(array):
    if array.dtype == 'complex128':
        show = np.log10(np.abs(array)).copy()
    else:
        show = array.copy()

    show = misc.imresize(show,0.5,interp='bicubic')
    pequ = Image.fromarray(show)
    img = ImageTk.PhotoImage(pequ)   
    imLabel.config(image=img)
    imLabel.image=img
def show_filter(H):
    H = misc.imresize(H,0.5,interp='bicubic')  
    pequ = Image.fromarray(H)
    img = ImageTk.PhotoImage(pequ)   
    filterLabel.config(image=img)
    filterLabel.image=img
def readfile():
    file = filedialog.askopenfilename(initialdir = '.\test images',filetypes =(("Image File", "*.jpg"),("Image File", "*.png"),("Image File", "*.gif"),
                                                   ("Image File", "*.bmp"),("All Files","*.*")),title = 'read file')
    img = mpimg.imread(file)
    global image_cache
    global ini_image_cache
    global homomor
    homomor = 0
    ini_image_cache = img
    image_cache = img
    show(img)
def savefile():
    global image_cache
    file = filedialog.asksaveasfilename(initialdir = '.\result',filetypes =(("Image File", "*.jpg"),("Image File", "*.png"),("Image File", "*.gif"),
                                                   ("Image File", "*.bmp"),("All Files","*.*")),title = 'save')
    if image_cache.dtype == 'complex128':
        save = np.log(np.abs(image_cache)+1)
    else:
        save = image_cache
    if len(save.shape)==2:
        plt.imsave(file,save,cmap='gray')
    else:
        plt.imsave(file,save)
def savefilter():
    global filter_cache
    file = filedialog.asksaveasfilename(initialdir = '.',filetypes =(("Image File", "*.jpg"),("Image File", "*.png"),("Image File", "*.gif"),
                                                   ("Image File", "*.bmp"),("All Files","*.*")),title = 'save filter')
    if filter_cache.dtype == 'complex128':
        save = np.abs(filter_cache)**(1/4)
    else:
        save = filter_cache
    plt.imsave(file,save,cmap='gray')   
def ini():
    global image_cache
    global ini_image_cache
    image_cache = ini_image_cache
    show(image_cache)
def fft():
    global image_cache
    if len(image_cache.shape) == 2:
        fourier_image = np.fft.fft2(image_cache)
        image_cache = fftpack.fftshift(fourier_image)
        show(np.log10(np.abs(image_cache)))
    elif len(image_cache.shape) == 3:
#        T = np.zeros_like(image_cache)
#        for k in range(3):
#            fourier_image = np.fft.fft2(image_cache[:,:,k])
#            T[:,:,k] = fftpack.fftshift(fourier_image)
#        image_cache = T
#        sh = (T[:,:,0]+T[:,:,1]+T[:,:,2])/3
#        show(np.log10(np.abs(sh)))
        
        image_hsv = colors.rgb_to_hsv(image_cache/255)
        fourier_image = np.fft.fft2(image_hsv[:,:,2])
        image_cache = fftpack.fftshift(fourier_image)
        show(np.log10(np.abs(image_cache)))
def ifft():
    global image_cache
    global ini_image_cache
    global homomor
    if len(ini_image_cache.shape) == 2:
        image_cache = fftpack.ifftshift(image_cache)
        image_cache = np.real(np.fft.ifft2(image_cache))
        if homomor == 1:
            image_cache = np.exp(image_cache)-1
            homomor = 0
            image_cache = np.uint8(image_cache)
        show(image_cache)
    elif len(ini_image_cache.shape) == 3:
        image_hsv = colors.rgb_to_hsv(ini_image_cache/255)
        image_cache = fftpack.ifftshift(image_cache)
        image_cache = np.real(np.fft.ifft2(image_cache))
        image_hsv[:,:,2] = image_cache
        image_rgb = colors.hsv_to_rgb(image_hsv)
        image_cache = image_rgb
        show(image_cache)
        
def D(u,v,u0,v0):
    return (((u-u0)**2)+((v-v0)**2))**(1/2)
def wiener():
    if weiner_var.get() == 'motion blur':
        degradation_motion_H()
        K=0.01
    elif weiner_var.get() == 'general blur':
        degradetion_blur()
        K=0.0001
    global image_cache
    global filter_cache  
    H = (1/filter_cache)*((np.abs(filter_cache)**2)/(np.abs(filter_cache)**2+K))
    filter_cache = H
    image_cache = H*image_cache
    show(np.log(np.abs(image_cache)+1))
    show_filter(np.abs(H)**(1/4))
def degradation_motion_H():
    global image_cache
    global filter_cache
    array = image_cache
    a=0.0155
    b=-0.0105
    t=0.5
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
    filter_cache = H
def degradetion_blur():
    global image_cache
    global filter_cache
    array = image_cache
    k=0.0001
    H=np.zeros(array.shape)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            u=i-array.shape[0]/2
            v=j-array.shape[1]/2
            H[i,j]=math.exp(-k*((u**2+v**2)**(5/6)))
    filter_cache = H
def ideal_high_pass():
    global image_cache
    global filter_cache
    global ini_image_cache
    global homomor
    homomor = 1
    array = image_cache
    D0=30
    H = np.ones(array.shape)
    u0 = array.shape[0]//2
    v0 = array.shape[1]//2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if D(i,j,u0,v0) <= D0:
                H[i,j] = 0
    filter_cache = H
    
    v = np.fft.fft2(np.log1p(ini_image_cache))
    img_fourier = fftpack.fftshift(v)
    image_cache = img_fourier*(0.75+1.25*H)
    
    show(np.log(np.abs(image_cache)+1))
    show_filter(H)
def butterworth_high_pass():
    global image_cache
    global filter_cache
    global ini_image_cache
    global homomor
    global homomor
    homomor = 1
    array = image_cache
    D0=30
    n=2
    H = np.ones(array.shape)
    u0 = array.shape[0]/2
    v0 = array.shape[1]/2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            H[i,j] = 1/(1+(D(i,j,u0,v0)/D0)**(2*n))
    H=1-H
    filter_cache = H
    
    v = np.fft.fft2(np.log1p(ini_image_cache))
    img_fourier = fftpack.fftshift(v)
    image_cache = img_fourier*(0.75+1.25*H)
    
    show(np.log(np.abs(image_cache)+1))
    show_filter(H)
def gaussian_high_pass():
    global image_cache
    global filter_cache
    global ini_image_cache
    global homomor
    homomor = 1
    array = image_cache
    D0=30
    H = np.ones(array.shape)
    u0 = array.shape[0]/2
    v0 = array.shape[1]/2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            H[i,j] = 1-math.exp(-(D(i,j,u0,v0)**2)/(2*(D0**2)))
    filter_cache = H
    
    v = np.fft.fft2(np.log1p(ini_image_cache))
    img_fourier = fftpack.fftshift(v)
    image_cache = img_fourier*(0.75+1.25*H)
    
    show(np.log(np.abs(image_cache)+1))
    show_filter(H)
def mynotch():
    global image_cache
    global filter_cache
    array = image_cache
    p1=np.array([[322,325]])
    p2=np.array([[702,699]])
    D0=float(notch_D0_entry.get())
#    D0=30
    H = np.ones(array.shape)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            D1 = D(i,j,p1[0,0],p1[0,1])
            D2 = D(i,j,p2[0,0],p2[0,1])
            if D1<=D0 or D2<=D0:
                H[i,j] = 0
    filter_cache = H
    image_cache = image_cache*H
    show(np.log(np.abs(image_cache)+1))
    show_filter(H)
def mygaussian_bandreject():
    global image_cache
    global filter_cache
    array = image_cache
    w=60
    C0=300
    H = np.ones(array.shape)
    u0 = array.shape[0]/2
    v0 = array.shape[1]/2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):          
            H[i,j] = 1-math.exp(-((D(i,j,u0,v0)**2-C0**2)/(D(i,j,u0,v0)*w))**2)
    
    filter_cache = H
    image_cache = image_cache*H
    show(np.log(np.abs(image_cache)+1))
    show_filter(H)
def myideal_bandreject():
    global image_cache
    global filter_cache
    array = image_cache
    w=60
    C0=300
    H = np.ones(array.shape)
    u0 = array.shape[0]//2
    v0 = array.shape[1]//2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if (C0-(w/2))<=D(i,j,u0,v0)<=(C0+(w/2)):
                H[i,j] = 0
    filter_cache = H
    image_cache = image_cache*H
    show(np.log(np.abs(image_cache)+1))
    show_filter(H)
def mybutterworth_bandreject():
    global image_cache
    global filter_cache
    array = image_cache
    w=60
    C0=300
    n=2
    H = np.ones(array.shape)
    u0 = array.shape[0]/2
    v0 = array.shape[1]/2
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):          
            H[i,j] = 1/(1+((D(i,j,u0,v0)*w)/(D(i,j,u0,v0)**2-C0**2))**(2*n))
    filter_cache = H
    image_cache = image_cache*H
    show(np.log(np.abs(image_cache)+1))
    show_filter(H)
def bandreject():
    if bandreject_var.get()=='ideal':
        myideal_bandreject()
    elif bandreject_var.get()=='butterworth':
        mybutterworth_bandreject()
    elif bandreject_var.get()=='gaussian':
        mygaussian_bandreject()


window = tk.Tk()
window.title('proj2')
window.geometry('1200x950')

frm_topic = tk.Frame(window)
frm_topic.pack(side='top')
frm_topicA = tk.Frame(frm_topic)
frm_topicA.grid(row=3,column=1,padx=5,pady=5)
frm_topicB = tk.Frame(frm_topic)
frm_topicB.grid(row=3,column=2,padx=5,pady=5)
frm_topicC = tk.Frame(frm_topic)
frm_topicC.grid(row=3,column=3,padx=5,pady=5)

frm_display = tk.Frame(window)
frm_display.pack(side='top')



title = tk.Label(frm_topic,text='Image Processing HW2\n何尚營(107064546)',bg='gray',font=('KaiTi',12),width=20,height=2)
title.grid(row=1,column=2,padx=5,pady=5)
topic_load = tk.Label(frm_topic,text='reading image file',bg='gray',font=('Arial',12),width=27,height=1)
topic_load.grid(row=2,column=1,padx=5,pady=5)

topicA = tk.Label(frm_topic,text='Image Restoration',bg='gray',font=('Arial',12),width=27,height=1)
topicA.grid(row=2,column=2,padx=5,pady=5)
topic_others = tk.Label(frm_topicA,text='Others',bg='gray',font=('Arial',12),width=27,height=1)
topic_others.grid(row=5,column=1,columnspan=2,padx=5,pady=5)
topicB = tk.Label(frm_topic,text='Homomorphic filtering',bg='gray',font=('Arial',12),width=27,height=1)
topicB.grid(row=2,column=3,padx=5,pady=5)
topic_fourier = tk.Label(frm_topicA,text='Fourier Transform',bg='gray',font=('Arial',12),width=27,height=1)
topic_fourier.grid(row=3,column=1,columnspan=2,padx=5,pady=5)

line_H = ttk.Separator(frm_topic, orient='horizontal')
line_H.grid(row=4,column=1,columnspan=3,sticky="we")

read_button = tk.Button(frm_topicA,text='read',width=10,height=2,command=readfile)
read_button.grid(row=2,column=1,padx=15,pady=5)
save_button = tk.Button(frm_topicA,text='save',width=10,height=2,command=savefile)
save_button.grid(row=2,column=2,padx=15,pady=5)
fft_button = tk.Button(frm_topicA,text='FFT',width=10,height=2,command=fft)
fft_button.grid(row=4,column=1,padx=15,pady=5)
ifft_button = tk.Button(frm_topicA,text='IFFT',width=10,height=2,command=ifft)
ifft_button.grid(row=4,column=2,padx=15,pady=5)

weiner_var=tk.StringVar()
weiner_mode = ttk.Combobox(frm_topicB,width=10,textvariable=weiner_var)
weiner_mode.config(values=('motion blur','general blur'))
weiner_mode.current(0)
weiner_mode.grid(row=2,column=1,columnspan=2,padx=5,pady=5)
weiner_button = tk.Button(frm_topicB,text='wiener filtering',width=20,height=2,command=wiener)
weiner_button.grid(row=2,column=3,padx=5,pady=5)

notch_D0_label = tk.Label(frm_topicB,text='D0:',font=('Arial',12),width=2,height=1)
notch_D0_label.grid(row=3,column=1,padx=1,pady=1)
notch_D0_entry = tk.Entry(frm_topicB,width=10)
notch_D0_entry.insert(tk.END,'30')
notch_D0_entry.grid(row=3,column=2,padx=1,pady=1)

notch_button = tk.Button(frm_topicB,text='notch filter',width=20,height=2,command=mynotch)
notch_button.grid(row=3,column=3,padx=5,pady=5)

bandreject_var=tk.StringVar()
bandreject_ideal_mode = ttk.Combobox(frm_topicB,width=10,textvariable=bandreject_var)
bandreject_ideal_mode.config(values=('ideal','butterworth','gaussian'))
bandreject_ideal_mode.current(0)
bandreject_ideal_mode.grid(row=4,column=1,columnspan=2,padx=5,pady=5)
bandreject_button = tk.Button(frm_topicB,text='band reject filter',width=20,height=2,command=bandreject)
bandreject_button.grid(row=4,column=3,padx=5,pady=5)

ini_button = tk.Button(frm_topicA,text='Initialize',width=10,height=2,command=ini)
ini_button.grid(row=6,column=1,padx=20,pady=5)
savefilter_button = tk.Button(frm_topicA,text='save filter',width=10,height=2,command=savefilter)
savefilter_button.grid(row=6,column=2,padx=20,pady=5)

ideal_highpass_button = tk.Button(frm_topicC,text='Ideal high pass filter',width=25,height=2,command=ideal_high_pass)
ideal_highpass_button.grid(row=2,column=1,padx=20,pady=5)
butterworth_highpass_button = tk.Button(frm_topicC,text='Butterworth high pass filter',width=25,height=2,command=butterworth_high_pass)
butterworth_highpass_button.grid(row=3,column=1,padx=20,pady=5)
gaussian_highpass_button = tk.Button(frm_topicC,text='Gaussian high pass filter',width=25,height=2,command=gaussian_high_pass)
gaussian_highpass_button.grid(row=4,column=1,padx=20,pady=5)

imLabel_topic = tk.Label(frm_display,text='Image',font=('Arial',15),width=10,height=1)
imLabel_topic.grid(row=1,column=1,padx=220,pady=1)
filterLabel_topic = tk.Label(frm_display,text='Filter',font=('Arial',15),width=10,height=1)
filterLabel_topic.grid(row=1,column=2,padx=220,pady=5)
#im_scale = tk.Scale(frm_display,from_=0.5,to=0.9,orient=tk.HORIZONTAL, length=200,resolution=0.1, tickinterval=0.1,command=scale_im)
#im_scale.grid(row=2,column=1,padx=5,pady=1)
imLabel=tk.Label(frm_display)
imLabel.grid(row=3,column=1,padx=5,pady=5)
filterLabel=tk.Label(frm_display)
filterLabel.grid(row=3,column=2,padx=5,pady=5)


window.mainloop()