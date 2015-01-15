'''
Created on Jan 4, 2015

@author: daqing_yi
'''

from RRTstarPlanner import *
import time

if __name__ == '__main__':
    
    def calcDist(currentPos, referencePos):
        dist = 0.0
        if referencePos==None:
            return dist
        dist = np.sqrt((currentPos[0]-referencePos[0])**2+(currentPos[1]-referencePos[1])**2)
        return dist   
    
        
    MAP_FILE = './map.png'
    
    planner = RRTstarPlanner([600, 400], 10, calcDist, MAP_FILE) 

    path = planner.findPath([40,40], [500, 40], 4000)
    print path
    
    import pygame.image
    pygame.image.save(planner.rrts_viz.screen, 'RRTstar02.png')
    
    while True:
        planner.rrts_viz.update()