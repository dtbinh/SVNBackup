'''
Created on Nov 3, 2014

@author: daqing_yi
'''

import pygame, sys
from pygame.locals import *
import pygame.image
import numpy as np

class MORRTVisualizer(object):

    def __init__(self, morrt, name=""):
        self.morrt = morrt
        self.name = name
        pygame.init()
        self.screen = pygame.display.set_mode((self.morrt.sampling_width,self.morrt.sampling_height))
        pygame.display.set_caption('MORRT')
        self.screen.fill((255,255,255))
        if self.morrt.mapfile != None:
            self.mapImg = pygame.image.load(self.morrt.mapfile)
        else:
            self.mapImg = None
        
        self.objImgs = []
            
        self.activePaths = []
        self.dispMap = True
        self.totalIdx = self.morrt.objectiveNum + self.morrt.subproblemNum
        self.currIdx = 0
        self.currImgs = 0
        self.pathIdx = 0
        
        self.font = pygame.font.SysFont(None, 24)
        
    def setName(self, name):
        self.name = name
    
        
    def loadObj(self, objFiles):    
        for obj in objFiles:
            self.objImgs.append(pygame.image.load(obj))

    def setLineColors(self, colors):
        self.lineColors = colors            
        
    def update(self):
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == pygame.K_UP:
                    self.currIdx += 1
                elif e.key == pygame.K_DOWN:
                    self.currImgs += 1
                elif e.key == pygame.K_RIGHT:
                    self.pathIdx += 1
                elif e.key == pygame.K_s:
                    pygame.image.save(self.screen, self.name+"-"+str(self.pathIdx)+".png")
            
            if self.currIdx >= self.totalIdx:
                self.currIdx = 0
            if self.currImgs >= len(self.objImgs):
                self.currImgs = 0
            if self.pathIdx >= len(self.activePaths):
                self.pathIdx = 0
            
        if self.objImgs[self.currImgs] != None:
            self.screen.blit(self.objImgs[self.currImgs],(0,0))
                
        disp_idx = 0
        if self.currIdx >= self.morrt.objectiveNum:
            disp_idx = self.currIdx - self.morrt.objectiveNum
            for n in self.morrt.subTrees[disp_idx].nodes:
                for c in n.children:
                    pygame.draw.line(self.screen, (128,200,0), n.pos, c.pos)
        else:
            disp_idx = self.currIdx
            for n in self.morrt.referenceTrees[disp_idx].nodes:
                for c in n.children:
                    pygame.draw.line(self.screen, (128,200,0), n.pos, c.pos)

                    
        pygame.draw.circle(self.screen, (255,0,0), self.morrt.start, 5)
        pygame.draw.circle(self.screen, (0,0,255), self.morrt.goal, 5)
        if self.morrt.new_pos != None and self.morrt.connected_pos != None:
            pygame.draw.line(self.screen, (200,128,0), self.morrt.new_pos, self.morrt.connected_pos)
            
        if len(self.activePaths) > 0:
            ap = self.activePaths[self.pathIdx]
            pathLen = len(ap)
            for i in range(0, pathLen-1, 1):
                pygame.draw.line(self.screen, (255, 160, 0), ap[i], ap[i+1], 2)
        
        '''
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Leaving because you requested it.")
        '''
        self.screen.blit(self.font.render("PI:"+str(self.pathIdx), True, (255,0,0)), (self.morrt.sampling_width-40, 10))
        self.screen.blit(self.font.render("TI:"+str(self.currIdx), True, (0,255,0)), (self.morrt.sampling_width-40, 40))
                
        pygame.display.flip();
        #pygame.time.delay(200)
        