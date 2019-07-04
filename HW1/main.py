from read_raw_file import read_raw_file
from gray_bmp import write_to_file
from my_imfilter import my_imfilter
from gauss2D import gauss2D

import numpy as np
import tkinter as tk
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from tkinter import filedialog
from skimage.transform import resize
#from skimage import exposure

def show(image_array):
    pgm_header = b'P5 '+ str(image_array.shape[1]).encode() + b' ' + str(image_array.shape[0]).encode() + b' ' + str(255).encode() + b' '
    image_array = np.asarray(image_array,dtype=np.uint8)
    img = tk.PhotoImage(data=pgm_header + bytes(image_array))    
    imLabel.config(image=img)
    imLabel.image=img
def readfile():
    file = filedialog.askopenfilename(initialdir = '.\data',filetypes =(("Image File", "*.raw"),("All Files","*.*")),title = 'read raw file')
    img = read_raw_file(file,512,512)
    global image_cache
    global ini_image_cache
    ini_image_cache = img
    image_cache = img
    show(img)
def savefile():
    global image_cache
    file = filedialog.asksaveasfilename(initialdir = '.\data',filetypes =(("24位元點陣圖(*.bmp)", "*.bmp"),("All Files","*.*")),title = 'save')
    write_to_file(file,image_cache)    
def sobel():
    global image_cache
    sobel_h = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
    sobel_v = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
    horizontal = my_imfilter(image_cache,sobel_h)
    vertical = my_imfilter(image_cache,sobel_v)
    image_cache = horizontal + vertical
    show(image_cache)
def laplacian():
    global image_cache
    kernel = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
    image_cache = image_cache + my_imfilter(image_cache,kernel)    
    show(image_cache)
def averag():
    global image_cache
    kernel = np.full((3,3),1/9)
    image_cache = my_imfilter(image_cache,kernel)
    show(image_cache)
def gaussian():
    global image_cache
    cutoff_frequency = 2
    gaussian_filter = gauss2D(shape=(cutoff_frequency*4+1,cutoff_frequency*4+1), sigma = cutoff_frequency)
    image_cache = my_imfilter(image_cache,gaussian_filter)
    show(image_cache)
def gaussian_noise():
    global image_cache    
    try:
        noise = np.random.normal(0,float(deviation_entry.get())**2,image_cache.shape)
        image_cache = noise + image_cache
        image_cache = np.around(image_cache)
        show(image_cache)
    except:
        print('invalid deviation value')        
def average_of_100gaussian_noise():
    global image_cache
    k = 0
    sum_of_noise_image = np.zeros_like(image_cache)
    try:
        variance = float(deviation_entry.get())**2
        noise = np.random.normal(0,variance,image_cache.shape)
        sum_of_noise_image = noise + image_cache      
        while k<99:
            noise = np.random.normal(0,variance,image_cache.shape)          
            sum_of_noise_image += (noise + image_cache)
            k += 1
        image_cache = sum_of_noise_image / 100
        image_cache = np.around(image_cache)
        show(image_cache)
    except:
        print('invalid deviation value')    
#def hist_equ():
#    global image_cache
#    image_cache = exposure.equalize_hist(image_cache)
#    image_cache = np.around(image_cache*255)
#    show(image_cache)
def ini():
    global image_cache
    global ini_image_cache
    image_cache = ini_image_cache
    show(image_cache)

ini_image_cache = np.empty((512,512))
image_cache = np.empty((512,512))

window = tk.Tk()
window.title('proj1')
window.geometry('850x900')

frm0 = tk.Frame(window)
frm0.pack(side='top')
frm1 = tk.Frame(frm0)
frm1.grid(row=4,column=1,padx=5,pady=5)
frm_topic = tk.Frame(frm1)
frm_topic.grid(row=2,column=1,padx=5,pady=5)
frm_targetC = tk.Frame(frm_topic)
frm_targetC.grid(row=2,column=3,padx=5,pady=5)

title = tk.Label(frm0,text='Image Processing HW1\n何尚營(107064546)',bg='gray',font=('KaiTi',12),width=20,height=2)
title.grid(row=1,column=1,padx=5,pady=5)
topicA = tk.Label(frm_topic,text='Reading Raw image file',bg='gray',font=('Arial',12),width=27,height=1)
topicA.grid(row=1,column=1,padx=5,pady=5)
topicB = tk.Label(frm_topic,text='Spatial filtering',bg='gray',font=('Arial',12),width=27,height=1)
topicB.grid(row=1,column=2,padx=5,pady=5)
topicC = tk.Label(frm_topic,text='Deniose',bg='gray',font=('Arial',12),width=30,height=1)
topicC.grid(row=1,column=3,padx=5,pady=5)

read_button = tk.Button(frm_topic,text='read',width=10,height=2,command=readfile)
read_button.grid(row=3,column=1,padx=15,pady=5)
save_button = tk.Button(frm_topic,text='save',width=10,height=2,command=savefile)
save_button.grid(row=4,column=1,padx=15,pady=5)
sobel_button = tk.Button(frm_topic,text='Sobel mask',width=20,height=2,command=sobel)
sobel_button.grid(row=2,column=2,padx=20,pady=5)
laplacian_button = tk.Button(frm_topic,text='Laplacian mask',width=20,height=2,command=laplacian)
laplacian_button.grid(row=3,column=2,padx=20,pady=5)
averaging_button = tk.Button(frm_topic,text='Averaging mask',width=20,height=2,command=averag)
averaging_button.grid(row=4,column=2,padx=20,pady=5)
gaussian_button = tk.Button(frm_topic,text='Gaussian mask',width=20,height=2,command=gaussian)
gaussian_button.grid(row=5,column=2,padx=20,pady=5)

gaussian_noise_button = tk.Button(frm_targetC,text='add Gaussian noise',width=15,height=2,command=gaussian_noise)
gaussian_noise_button.grid(row=1,column=1,padx=1,pady=5)
gaussian_noise_label = tk.Label(frm_targetC,text='deviation:',font=('Arial',12),width=8,height=2)
gaussian_noise_label.grid(row=1,column=2,padx=1,pady=5)
deviation_entry = tk.Entry(frm_targetC,width=10)
deviation_entry.grid(row=1,column=3,padx=1,pady=5)

topic_others = tk.Label(frm_topic,text='Others',bg='gray',font=('Arial',12),width=20,height=1)
topic_others.grid(row=4,column=3,padx=5,pady=5)
ave_of_100gaussian_button = tk.Button(frm_topic,text='average of 100 gaussian noise',width=25,height=2,command=average_of_100gaussian_noise)
ave_of_100gaussian_button.grid(row=3,column=3,padx=5,pady=5)
initialize_button = tk.Button(frm_topic,text='Initialize',width=20,height=2,command=ini)
initialize_button.grid(row=5,column=3,padx=5,pady=5)

#hist_equ_button = tk.Button(frm_topic,text='hist',width=25,height=2,command=hist_equ)
#hist_equ_button.grid(row=6,column=3,padx=5,pady=5)

imLabel=tk.Label(frm0)
imLabel.grid(row=8,column=1,padx=5,pady=5)

window.mainloop()

#main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#image = read_raw_file(os.path.abspath('.\data\lena.raw'),512,512)
#image1 = sk.util.random_noise(image,mode='gaussian',var=0.01)
#result = ndimage.sobel(image1,mode='mirror')
#plt.figure(1)
#plt.imshow(image,cmap=cm.gray)
#plt.figure(2)
#plt.imshow(image1,cmap=cm.gray)
#plt.figure(3)
#plt.imshow(result,cmap=cm.gray)
#plt.show()
