# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 13:23:48 2018

@author: sun
"""

import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import math
import numpy as np
from PIL import Image, ImageTk
from matplotlib import pyplot as plt

from arithmetic_encoding import ar_encoding
from compute_entropy import entropy, horizontal_entropy, horizontal_entropy_fast
from huffman_encoding import huffman
from lzw import lzw_encoding, inidict
from recover import recover_row, recover_col


def show(array):
    pequ = Image.fromarray(array)
    img = ImageTk.PhotoImage(pequ)   
    imLabel.config(image=img)
    imLabel.image=img
def entropy_update():
    global image_cache  
    try:
        entropy_var.set('entropy='+'computing...')       
        entropy_var.set('entropy='+str(entropy(image_cache)))     
    except:
        entropy_var.set('entropy='+'fail to compute')  
    
    try:
        h_entropy_var.set('horizontal difference entropy='+'computing...')
        h_entropy_var.set('horizontal difference entropy='+str(horizontal_entropy_fast(image_cache)))    
    except:
        if image_cache.ndim != 2:
            h_entropy_var.set('horizontal difference entropy='+'Only 2D arrays with a channels axis are supported')
        else:
            h_entropy_var.set('horizontal difference entropy='+'fail to compute')
def readfile():
    file = filedialog.askopenfilename(initialdir = '.\test images',filetypes =(("Image File", "*.jpg"),("Image File", "*.png"),("Image File", "*.gif"),
                                                   ("Image File", "*.bmp"),("All Files","*.*")),title = 'read file')
    try:
        img = plt.imread(file)
        global image_cache
        image_cache = img
        show(img)
        sub = threading.Thread(target=entropy_update)
        sub.start()
    except:
        print('fail to read file')
def huffman_encode():
    global image_cache
    compression_ratio = huffman(image_cache)
    huf_var.set(compression_ratio)
def arithmetic_encode():
    global image_cache
    compression_ratio,codeword = ar_encoding(image_cache)
    ari_var.set(compression_ratio)
def lzw_encode():
    global image_cache
    codeword,dictnary = lzw_encoding(image_cache.flatten(),inidict())
    bit_per_word = math.ceil(math.log2(len(dictnary)))
    compression_ratio = 8/(len(codeword)*bit_per_word/len(image_cache.flatten()))
    lzw_var.set(compression_ratio)
def recover_r():
    global image_cache
    recover_image = recover_row(image_cache)
    image_cache = recover_image
    sub = threading.Thread(target=entropy_update)
    sub.start()
    show(image_cache)
    plt.imsave('./result/3_recover.jpg',recover_image,cmap='gray')
def recover_c():
    global image_cache
    recover_image = recover_col(image_cache)
    image_cache = recover_image
    sub = threading.Thread(target=entropy_update)
    sub.start()
    show(image_cache)
    plt.imsave('./result/4_recover.jpg',recover_image,cmap='gray')

window = tk.Tk()
window.title('proj3')
window.geometry('800x980')

frm0 = tk.Frame(window)
frm0.pack(side='top')
frm1 = tk.Frame(frm0)
frm1.grid(row=3,column=1,padx=5,pady=5)
frm_coding = tk.Frame(frm1)
frm_coding.grid(row=1,column=1,padx=5,pady=5)
frm_recover = tk.Frame(frm1)
frm_recover.grid(row=2,column=1,padx=5,pady=5)
frm_entropy = tk.Frame(frm0)
frm_entropy.grid(row=5,column=1,padx=5,pady=5)

title = tk.Label(frm0,text='Digital Image Processing HW3\nShang-Ying,He(107064546)',bg='gray',font=('Arial',12),width=30,height=2)
title.grid(row=1,column=1,padx=5,pady=5)
read_button = tk.Button(frm0,text='read image',width=20,height=2,command=readfile)
read_button.grid(row=2,column=1,padx=15,pady=5)

topicA = tk.Label(frm_coding,text='Image Coding',bg='gray',font=('Arial',12),width=50,height=1)
topicA.grid(row=1,column=1,columnspan=3,padx=5,pady=5)
Huffman_button = tk.Button(frm_coding,text='Huffman Coding',width=15,height=2,command=huffman_encode)
Huffman_button.grid(row=2,column=1,padx=5,pady=5)
Arithmetic_button = tk.Button(frm_coding,text='Arithmetic Coding',width=15,height=2,command=arithmetic_encode)
Arithmetic_button.grid(row=2,column=2,padx=5,pady=5)
lzw_button = tk.Button(frm_coding,text='LZW Coding',width=15,height=2,command=lzw_encode)
lzw_button.grid(row=2,column=3,padx=5,pady=5)

compression_ratio_label=tk.Label(frm_coding,text='compression ratio')
compression_ratio_label.grid(row=3,column=1,columnspan=3,padx=5,pady=1)
huf_var=tk.StringVar()
huf_var.set(0.0)
ari_var=tk.StringVar()
ari_var.set(0.0)
lzw_var=tk.StringVar()
lzw_var.set(0.0)
huf_label=tk.Label(frm_coding,textvariable=huf_var)
huf_label.grid(row=4,column=1,padx=5,pady=1)
ari_label=tk.Label(frm_coding,textvariable=ari_var)
ari_label.grid(row=4,column=2,padx=5,pady=1)
lzw_label=tk.Label(frm_coding,textvariable=lzw_var)
lzw_label.grid(row=4,column=3,padx=5,pady=1)

topicB = tk.Label(frm_recover,text='Image Permutation',bg='gray',font=('Arial',12),width=50,height=1)
topicB.grid(row=1,column=1,columnspan=2,padx=5,pady=5)
recover_row_button = tk.Button(frm_recover,text='recover(row)',width=15,height=2,command=recover_r)
recover_row_button.grid(row=2,column=1,padx=20,pady=5)
recover_col_button = tk.Button(frm_recover,text='recover(column)',width=15,height=2,command=recover_c)
recover_col_button.grid(row=2,column=2,padx=20,pady=5)

line_H = ttk.Separator(frm0, orient='horizontal')
line_H.grid(row=4,column=1,columnspan=3,sticky="we")

entropy_var=tk.StringVar()
entropy_var.set('entropy='+str(0.0))
h_entropy_var=tk.StringVar()
h_entropy_var.set('horizontal difference entropy='+str(0.0))
entropy_label=tk.Label(frm_entropy,textvariable=entropy_var)
entropy_label.grid(row=1,column=1,padx=5,pady=1)
h_entropy_label=tk.Label(frm_entropy,textvariable=h_entropy_var)
h_entropy_label.grid(row=2,column=1,padx=5,pady=1)

imLabel=tk.Label(frm0)
imLabel.grid(row=8,column=1,padx=5,pady=5)

window.mainloop()