import numpy as np
import struct

def read_raw_file(path,height,width):
    f = open(path,'rb').read()
    v = struct.unpack('='+'B'*len(f),f)
    img = (np.asarray(v,dtype=np.uint8)).reshape(height,width)
    return img