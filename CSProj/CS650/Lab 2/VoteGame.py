'''
Created on Sep 23, 2014

@author: daqing_yi
'''
import numpy as np

class Vote(object):
    
    def __init__(self, accumulator, voter, weight):
        self.accumulator = accumulator
        self.voter = voter
        self.weight = weight
        
class Voter(object):
    
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.votes = []
        
    def getWeightedVoteSum(self):
        weightedSum = 0.0
        for v in self.votes:
            weightedSum += v.weight        
        return weightedSum

class Accumulator(object):
    
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.votes = []
        
    def addVote(self, vote):
        self.votes.append(vote)
        
    def getWeightedVoteSum(self):
        weightedSum = 0.0
        for v in self.votes:
            weightedSum += v.weight        
        return weightedSum

class AccumulatorMgr(object):

    def __init__(self):
        self.accumulators = []
        
    def findAccumulator(self, x, y, r):
        for a in self.accumulators:
            if a.x==x and a.y==y and a.r==r:
                return a
        return None
    
class VoterMgr(object):
    
    def __init__(self):
        self.voters =[]
        
    def findVoter(self, pos_x, pos_y):
        for v in self.voters:
            if v.pos_x == pos_x and v.pos_y == pos_y:
                return v
        return None

        
class VoteGame(object):
    
    def __init__(self, width, height, radii):
        self.width = width
        self.height = height
        self.radii = radii
        
        self.accumulatorMgr = AccumulatorMgr()
        self.voterMgr = VoterMgr()
        self.votes = []
        
        
    def vote(self, x, y, r, voter_x, voter_y, weight=1):
        voter = self.voterMgr.findVoter(voter_x, voter_y)
        if voter==None:
            voter = Voter(voter_x, voter_y)
            self.voterMgr.voters.append(voter)
            
        accumulator = self.accumulatorMgr.findAccumulator(x, y, r)
        if accumulator==None:
            accumulator = Accumulator(x, y, r)
            self.accumulatorMgr.accumulators.append(accumulator)
            
        vote = Vote(accumulator, voter, weight)
        voter.votes.append(vote)
        accumulator.votes.append(vote)
        
    def dumpHoughImg(self):
        
        hough_img = np.zeros((self.width, self.height, len(self.radii)), np.float)
        
        for a in self.accumulatorMgr.accumulators:
            hough_img[a.x, a.y, a.r] = a.getWeightedVoteSum()
            
        return hough_img
    
    def dumpHoughImgByRadusIndex(self, r_idx):
        
        hough_img = np.zeros((self.width, self.height), np.float)
        
        for a in self.accumulatorMgr.accumulators:
            if a.r == self.radii[r_idx]:
                hough_img[a.x, a.y] = a.getWeightedVoteSum()
            
        return hough_img
        
        