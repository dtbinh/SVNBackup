'''
Created on Nov 2, 2014

@author: daqing_yi
'''

from PixelGraph import *
from ShapeClassifier import *

if __name__ == '__main__':
    
    img1_file = "shapes.pgm"
    img2_file = "testshapes.pgm"
    img1 = cv2.imread(img1_file, 0)
    img2 = cv2.imread(img2_file, 0)
    print img1.shape
    print img2.shape

    img1_bi = 1*(img1 >= 100)
    img2_bi = 1*(img2 >= 100)
    
    pxg1 = PixelGraph(img1_bi)
    pxg2 = PixelGraph(img2_bi)
    
    cluster_num = 5
    feature_num = 2
    shpXfier = ShapeClassifier(feature_num, cluster_num)
    
    for s in pxg1.shapeDescriptors:
        shpXfier.addShape(s)
    for s in pxg2.shapeDescriptors:
        shpXfier.addShape(s)
        
    shpXfier.classify()
    
    colors = [(255,0,0), (0,255,0), (0,0,255),(255,122,0),(0,122,122)]
    pxg1.visualizeByLabel("pxg1", colors)
    pxg2.visualizeByLabel("pxg2", colors)
    