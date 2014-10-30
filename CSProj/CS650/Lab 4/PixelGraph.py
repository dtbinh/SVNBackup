'''
Created on Oct 27, 2014

@author: daqing_yi
'''

#http://en.wikipedia.org/wiki/Connected-component_labeling

import numpy as np
import cv2
import csv
import matplotlib.pyplot as plt

from ConnectedComponent import *
from ShapeDescriptor import *

class PixelGraph(object):

    def __init__(self, data):
        
        self.width = data.shape[0]
        self.height = data.shape[1]
        self.componentMgr = ConnectedComponentMgr(data)
        
        self.shapeDescriptors = []
        self.componentNum = self.componentMgr.getComponentNum()
        for idx in range(self.componentNum):
            self.shapeDescriptors.append(ShapeDescriptor(self.componentMgr.getComponentLabelData(idx)))
   
    
    def visualize(self, name):
        
        color_img = np.zeros((self.width, self.height, 3), np.int)
        componenet_num = self.componentMgr.getComponentNum()
        r_vals = np.random.randint(0, 256, componenet_num)
        g_vals = np.random.randint(0, 256, componenet_num)
        b_vals = np.random.randint(0, 256, componenet_num)  
        
        for i in range(self.width):
            for j in range(self.height):
                if self.componentMgr.labelData[i,j] >= 0:
                    idx = self.componentMgr.labelData[i, j]
                    color_img[i, j, 0] = r_vals[idx]
                    color_img[i, j, 1] = g_vals[idx]
                    color_img[i, j, 2] = b_vals[idx]
                else:
                    color_img[i, j, 0] = 255
                    color_img[i, j, 1] = 255
                    color_img[i, j, 2] = 255
                            
        plt.imshow(color_img)
        plt.show()
        
        
    def visualizeComponent(self, name, idx):
        
        color_img = np.zeros((self.width, self.height, 3), np.int)
        r_val = np.random.randint(0, 256)
        g_val = np.random.randint(0, 256)
        b_val = np.random.randint(0, 256)  
        
        for c in self.componentMgr.components[idx]:
            color_img[c[0], c[1], 0] = r_val
            color_img[c[0], c[1], 1] = g_val
            color_img[c[0], c[1], 2] = b_val
                            
        plt.imshow(color_img)
        plt.show()
        
    def visualizeComponentChainCode(self, name, idx):
        
        color_img = np.zeros((self.width, self.height, 3), np.int)

        cc, chain = self.shapeDescriptors[idx].findChainCode()
        for c in chain:
            color_img[c[0], c[1], 0] = 122
            color_img[c[0], c[1], 1] = 122
            color_img[c[0], c[1], 2] = 122   
                            
        plt.imshow(color_img)
        plt.show() 
        
    def visualizeComponentBoundary(self, name, idx):
        color_img = np.zeros((self.width, self.height, 3), np.int)
        bp = self.shapeDescriptors[idx].getBoundaryPixel()  
        for c in bp:
            color_img[c[0], c[1], 0] = 255
            color_img[c[0], c[1], 1] = 122
            color_img[c[0], c[1], 2] = 122   
                            
        plt.imshow(color_img)
        plt.show()     
        
    def visualizeConvexHull(self, name, idx):
        
        fig = plt.figure()
        ax = fig.add_subplot(111)

        bp = self.shapeDescriptors[idx].getBoundaryPixel()  
        for c in bp:
            ax.plot(c[0], c[1], 'bx')
 
        convexHull = self.shapeDescriptors[idx].getConvexHull()
        hull_num = len(convexHull)
        if hull_num > 0:
            for i in range(hull_num-1):
                ax.plot([convexHull[i][0], convexHull[i+1][0]], [convexHull[i][1], convexHull[i+1][1]], 'r-')
            ax.plot([convexHull[hull_num-1][0], convexHull[0][0]], [convexHull[hull_num-1][1], convexHull[0][1]], 'r-')
        
        
        plt.show()
        
    def visualizeMinimumBoundingRect(self, name, id):
        
        pass
        
    def dump(self, filename):
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(self.componentMgr.labelData)
        
        
                     

        