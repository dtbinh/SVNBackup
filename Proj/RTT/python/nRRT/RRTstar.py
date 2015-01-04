'''
Created on Jan 3, 2015

@author: daqing_yi
'''

from RRG import *

class RRTstar(RRG):

    def __init__(self, sampling_range, segmentLength):
        super(RRTstar, self).__init__(sampling_range, segmentLength)
        self.costFunc = None
        
    def init(self, start, goal, costFunc):
        super(RRTstar, self).init(start, goal)
        self.costFunc = costFunc
        self.root.cost = self.costFunc(self.root, None)
        
    def extend(self):
        new_node = None
        while new_node == None:
            rndPos = self.sampling()
            nearest_node = self.findNearestNeighbor(rndPos)
            
            new_pos = self.steer(rndPos, nearest_node.pos)
            
            if True == self.isObstacleFree(nearest_node.pos, new_pos):
                new_node = RRTNode(new_pos)
                self.kdtree_root.add(new_pos, new_node)
                
                new_node.cost = nearest_node.cost + self.costFunc(new_node, nearest_node)
                self.nodes.append(new_node)
                
                min_node = nearest_node
                self.addEdge(min_node, new_node)
                
                near_node_list = self.findNearVertices(new_node.pos, self.nearNodeNum)
                for near_node in near_node_list:
                    if near_node == min_node:
                        continue
                    
                    if True == self.isObstacleFree(near_node.pos, new_node.pos):
                        
                        c = self.getCostToNode(near_node) + self.costFunc(near_node, new_node)
                        if c < self.getCostToNode(new_node):
                            parent_node = self.getParent(near_node)
                            self.removeEdge(parent_node, near_node)
                            self.addEdge(new_node, near_node)
                
                            
                            
    def getCostToNode(self, node):
        return node.cost
    
    def getParent(self, node):
        return node.parent
                 
                        
    def removeEdge(self, node_p, node_c):
        ret = super(RRTstar, self).removeEdge(node_p, node_c)
        if ret == False:
            return False
        node_c.parent = None
        return True
    
    def addEdge(self, node_p, node_c):
        ret = super(RRTstar, self).addEdge(node_p, node_c)
        if ret == False:
            return False
        node_c.parent = node_p
        return True
                            

                        
                
        
        
    
