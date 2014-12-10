'''
Created on Dec 7, 2014

@author: daqing_yi
'''

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from LDASampler import *

type_str = ["Agents", "AI", "DB", "IR", "ML", "HCI"]

def getIndex(input):
    if input==type_str[0]:
        return 0
    if input==type_str[1]:
        return 1
    if input==type_str[2]:
        return 2
    if input==type_str[3]:
        return 3
    if input==type_str[4]:
        return 4
    if input==type_str[5]:
        return 5
    return -1
    
if __name__ == '__main__':
    
    citeseer_content = np.loadtxt('citeseer.content', delimiter='\t', dtype=str)
    print citeseer_content.shape   
    
    row_num = citeseer_content.shape[0]
    col_num = citeseer_content.shape[1]
    
    print row_num
    print col_num
    
    data_mat = np.zeros((row_num, col_num-2))
    doc_list = []
    type_list = np.zeros(row_num, dtype=np.int)
    for i in range(row_num):
        doc_list.append(citeseer_content[i][0])
        for j in range(1, col_num-1):
            data_mat[i,j-1] = int(citeseer_content[i][j])
        type_list[i] = getIndex(citeseer_content[i][col_num-1])
    
    print data_mat.shape
    print len(doc_list)
    print type_list.shape
    
    TOPIC_NUM = row_num
    ITERATION_NUM = 10
    
    print "Start sampling ......"
    
    sampler = LDASampler(TOPIC_NUM, alpha=6.667)
    for it, phi in enumerate(sampler.run(data_mat, ITERATION_NUM)):
        print "Iteration", it
        likelihood = sampler.loglikelihood()
        print "Likelihood " + str(likelihood)
        
    theta = sampler.theta()
    theta_i = np.argmax(theta,axis=1) + 1
    
    print theta.shape
    print theta_i.shape
    
    wrong_cnt = 0
    for i in range(theta_i.shape[0]):
        if theta_i[i] != type_list[i]:
            wrong_cnt += 1
    print " wrong cnt " + str(wrong_cnt)
    
    
    
            
    
    