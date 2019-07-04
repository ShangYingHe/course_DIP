import numpy as np
import struct
import os

header = {'type':'BM','size':786486,'reserved1':0,'reserved2':0,'offset':54,
          'DIB header size':40,'width':512,'height':512,'color planes':1,'bit per pixel':24,'compression method':0,
          'raw image size':786432,'horizontal resolution':0,'vertical resolution':0,'number of colors':0,'important colors':0}

def make_header():
    header_str = b''
    header_str += header['type'].encode()
    header_str += struct.pack('<L', header['size'])     
    header_str += struct.pack('=H', header['reserved1'])
    header_str += struct.pack('=H', header['reserved2'])
    header_str += struct.pack('<L', header['offset'])
    header_str += struct.pack('<L', header['DIB header size'])
    header_str += struct.pack('<L', header['width'])
    header_str += struct.pack('<L', header['height'])
    header_str += struct.pack('<H', header['color planes'])
    header_str += struct.pack('<H', header['bit per pixel'])
    header_str += struct.pack('<L', header['compression method'])
    header_str += struct.pack('<L', header['raw image size'])
    header_str += struct.pack('<L', header['horizontal resolution'])
    header_str += struct.pack('<L', header['vertical resolution'])
    header_str += struct.pack('<L', header['number of colors'])
    header_str += struct.pack('<L', header['important colors'])
    return header_str
def reverse(img):
    output = np.zeros_like(img)
    for i in range(img.shape[0]):
        output[output.shape[0]-1-i,:] = img[i,:]
    return output
def write_to_file(filename,image):
    image = np.asarray(image,dtype=np.uint8)            
    try:        
        if filename.endswith('.bmp') == False:
            filename += '.bmp'
        test = open(filename,'wb')
        test.write(make_header() + bytes(reverse(image).repeat(3)))
        test.close()
    except:
        print('path format error')

###### header test ######
#bmp = open(r'temp\HW1\data\1.bmp', 'rb')
#print('Type:', bmp.read(2).decode())
#print('Size: %s' % struct.unpack('I', bmp.read(4)))
#print('Reserved 1: %s' % struct.unpack('H', bmp.read(2)))
#print('Reserved 2: %s' % struct.unpack('H', bmp.read(2)))
#print('Offset: %s' % struct.unpack('I', bmp.read(4)))
#
#print('DIB Header Size: %s' % struct.unpack('I', bmp.read(4)))
#print('Width: %s' % struct.unpack('I', bmp.read(4)))
#print('Height: %s' % struct.unpack('I', bmp.read(4)))
#print('Colour Planes: %s' % struct.unpack('H', bmp.read(2)))
#print('Bits per Pixel: %s' % struct.unpack('H', bmp.read(2)))
#print('Compression Method: %s' % struct.unpack('I', bmp.read(4)))
#print('Raw Image Size: %s' % struct.unpack('I', bmp.read(4)))
#print('Horizontal Resolution: %s' % struct.unpack('I', bmp.read(4)))
#print('Vertical Resolution: %s' % struct.unpack('I', bmp.read(4)))
#print('Number of Colours: %s' % struct.unpack('I', bmp.read(4)))
#print('Important Colours: %s' % struct.unpack('I', bmp.read(4)))