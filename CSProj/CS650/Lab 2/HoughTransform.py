'''
Created on Sep 17, 2014

@author: daqing_yi
'''
import numpy as np
from VoteGame import *


def houghCircle(bi_img, radii):
    radiiLen = len(radii)
    radiiMax = np.max(radii)
    
    img_width = bi_img.shape[0]
    img_height = bi_img.shape[1]
    
    vote_game = VoteGame(img_width+radiiMax, img_height+radiiMax, radii)
    
    for r in radii:
        for i in range(img_width):
            for j in range(img_height):
                if bi_img[i,j] > 0:
                    pixels = getCircleEdgePixels([i,j], r)
                    for pix in pixels:
                        pix_x, pix_y = pix[0], pix[1]
                        if pix_x >= -r and pix_x < img_width+r and pix_y >= -r and pix_y < img_height+r:
                            vote_game.vote(pix_x, pix_y, r, i, j)
                                      
    return vote_game

def oneVoterPerVoteMethod(vote_game, img_data):
    pass

def recursiveWeightedVoteMethod(vote_game, img_data):
    pass

def weightedRevote(vote_game):
                
    for voter in vote_game.voterMgr.voters:
        weightSum = voter.getWeightedVoteSum()
        for v in voter.votes:
            v.weight /= weightSum
            
    return vote_game
        

def findByThreshold(img_data, threshold):
    
    results = []
    img_width = img_data.shape[0]
    img_height = img_data.shape[1]
    
    for i in range(img_width):
        for j in range(img_height):
            if img_data[i,j] > threshold:
                results.append([i,j])
    return results


def findLocalMax(hough_img):
    local_max = []
    
    hough_img_min = np.min(np.min(hough_img))
    hough_img_max = np.max(np.max(hough_img))
    img_width = hough_img.shape[0]
    img_height = hough_img.shape[1]
    
    print hough_img_min
    print hough_img_max
    
    threshold = 0.9 *(hough_img_max - hough_img_min) + hough_img_min
    
    for i in range(img_width):
        for j in range(img_height):
            if hough_img[i,j] > threshold:
                local_max.append([i,j])
                
    return local_max
        

def getCircleEdgePixels(center, radius):
    pixels = []
    for theta in range(0, 360, 2):
        theta_radius = theta*np.pi/180.0
        x = int(center[0] + radius * np.cos(theta_radius))
        y = int(center[1] + radius * np.sin(theta_radius))
        if [x,y] not in pixels:
            pixels.append([x, y])

    return pixels


