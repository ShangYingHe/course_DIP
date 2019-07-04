import numpy as np

def my_imfilter(image, imfilter):
    output = np.zeros_like(image)
#    imfilter = np.rot90(imfilter,k=2)  #180 degree rotation of the filter matrix
    image = np.lib.pad(image,((imfilter.shape[0]//2,imfilter.shape[0]//2),
                              (imfilter.shape[1]//2,imfilter.shape[1]//2)),'constant',constant_values=0)    #zero padding

    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            output[i,j]=(imfilter*image[i:i+imfilter.shape[0],j:j+imfilter.shape[1]]).sum()
    
    return output