'''
Created on Jan 23, 2015

@author: daqing_yi
'''

from WorldMapMgr import *

if __name__ == '__main__':
    
    MAP_FILE = 'map01.jpg'
    mapMgr = WorldMapMgr()
    mapMgr.load(MAP_FILE)
    
    while True:
        mapMgr.visualize()