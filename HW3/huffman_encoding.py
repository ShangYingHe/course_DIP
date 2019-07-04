# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 00:22:11 2018

@author: sun
"""
import numpy as np
import queue
from matplotlib import pyplot as plt

class Node:
    def __init__(self):
        self.prob = None
        self.code = None
        self.data = None
        self.left = None
        self.right = None
    def __lt__(self,other):
        if self.prob < other.prob:
            return 1
        else:
            return 0
    def __ge__(self,other):
        if self.prob > other.prob:
            return 1
        else:
            return 0      
def tree(pb):
    prior_que = queue.PriorityQueue()
    for intensity,prob in enumerate(pb):
        leaf = Node()
        leaf.data = intensity
        leaf.prob = prob
        prior_que.put(leaf)
    while prior_que.qsize() > 1:
        newnode = Node()
        l = prior_que.get()
        r = prior_que.get()
        newnode.left = l
        newnode.right = r
        newprob = l.prob + r.prob
        newnode.prob = newprob
        prior_que.put(newnode)
    return prior_que.get()
def huffman_traversal(root_node,tmp_array,f):		# traversal of the tree to generate codes
    if (root_node.left is not None):
        tmp_array[huffman_traversal.count] = 1
        huffman_traversal.count+=1
        huffman_traversal(root_node.left,tmp_array,f)
        huffman_traversal.count-=1
    if (root_node.right is not None):
        tmp_array[huffman_traversal.count] = 0
        huffman_traversal.count+=1
        huffman_traversal(root_node.right,tmp_array,f)
        huffman_traversal.count-=1
    else:
        huffman_traversal.output_bits[root_node.data] = huffman_traversal.count		#count the number of bits for each color
        bitstream = ''.join(str(cell) for cell in tmp_array[1:huffman_traversal.count]) 
        color = str(root_node.data)
        wr_str = color+' '+ bitstream+'\n'
        f.write(wr_str)
    return
def huffman(image):
    hist = np.bincount(image.flatten(),minlength=256)
    pb = hist/np.sum(hist)
    root_node = tree(pb)
    tmp_array = np.ones([64],dtype=int)
    huffman_traversal.output_bits = np.empty(256,dtype=int) 
    huffman_traversal.count = 0
    f = open('./result/huffman_codes.txt','w')
    huffman_traversal(root_node,tmp_array,f)
    compression_ratio = 8/(np.sum(huffman_traversal.output_bits*hist)/image.size)
    return compression_ratio

if __name__ == '__main__':
    image = plt.imread('./data/image2.bmp')
    compression_ratio = huffman(image)
    print(compression_ratio)