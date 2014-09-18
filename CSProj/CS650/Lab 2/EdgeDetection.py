'''
Created on Sep 17, 2014

@author: daqing_yi
'''
import numpy as np

def discretizeAngle(angle):
    
    d_angle = 0.0
    if angle <= np.pi/8 and angle > -np.pi/8:
        d_angle = 0.0
    elif angle <= 3 *np.pi/8 and angle > np.pi/8:
        d_angle = np.pi/4
    elif angle <= 5 * np.pi/8 and angle > 3 * np.pi/4:
        d_angle = np.pi/2
    elif angle <= 7 * np.pi/8 and angle > 5 * np.pi/8:
        d_angle = 3 * np.pi/4
    elif (angle <= np.pi and angle > 7 * np.pi/8) or (angle <= -7 * np.pi/8 and angle >= - np.pi):
        d_angle = - np.pi
    elif angle <= - 5 * np.pi/8 and angle > -7 * np.pi/8:
        d_angle = - 3 * np.pi/4
    elif angle <= - 3 * np.pi/8 and angle > - 5 * np.pi/8:
        d_angle = - np.pi/2
    elif angle <= - np.pi/8 and angle > - 3 * np.pi/8:
        d_angle = - np.pi/4
        
    return d_angle
        
    

def sobel(img_data):
    
    img_width = img_data.shape[0]
    img_height = img_data.shape[1]
        
    sobel_x_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y_kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    gradient_x = np.zeros(img_data.shape, np.float)
    gradient_y = np.zeros(img_data.shape, np.float)
    gradient_magnitude = np.zeros(img_data.shape, np.float)
    gradient_orientation = np.zeros(img_data.shape, np.float)
    
    for i in range(1, img_width-1):
        for j in range(1, img_height-1):
            
            img_data_seg = np.array(img_data[i-1:i+2, j-1:j+2])
            gradient_x[i,j] = np.sum( np.sum( sobel_x_kernel * img_data_seg ) )
            gradient_y[i,j] = np.sum( np.sum( sobel_y_kernel * img_data_seg ) )
            gradient_magnitude[i,j] = np.sqrt(gradient_x[i,j]**2 + gradient_y[i,j]**2)
            gradient_orientation[i,j] = discretizeAngle( np.arctan2(gradient_y[i,j], gradient_x[i,j]) )
            
    return gradient_magnitude, gradient_orientation

def laplacian(img_data):
            
    img_width = img_data.shape[0]
    img_height = img_data.shape[1]
     
    laplacian_kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])    
    hessian = np.zeros(img_data.shape, np.float)
    
    for i in range(1, img_width-1):
        for j in range(1, img_height-1):
            
            img_data_seg = np.array(img_data[i-1:i+2, j-1:j+2])
            hessian[i, j] = np.sum( np.sum( img_data_seg * laplacian_kernel ) )
            
    return hessian

def canny(img_data):
    
    img_width = img_data.shape[0]
    img_height = img_data.shape[1]
    
    img_gm, img_go = sobel(img_data)
    hessian = laplacian(img_data)
    
    img_can = np.zeros(img_data.shape, np.float)
    
    img_gm_min = np.min(np.min(img_gm))
    img_gm_max = np.max(np.max(img_gm))
    threshold = (img_gm_max - img_gm_min) * 0.2 + img_gm_min
    
    print threshold
    
    for i in range(1, img_width-1):
        for j in range(1, img_height-1):
            
            if img_gm[i, j] > threshold:            
                if img_go[i,j] == 0:
                    delta_i = 1
                    delta_j = 0
                elif img_go[i,j] == np.pi/4:
                    delta_i = 1
                    delta_j = 1
                elif img_go[i,j] == np.pi/2:
                    delta_i = 0
                    delta_j = 1
                elif img_go[i,j] == 3*np.pi/4:
                    delta_i = -1
                    delta_j = 1
                elif img_go[i,j] == - np.pi:
                    delta_i = -1
                    delta_j = 0
                elif img_go[i,j] == - 3*np.pi/4:
                    delta_i = -1
                    delta_j = -1
                elif img_go[i,j] == - np.pi/2:
                    delta_i = 0
                    delta_j = -1
                elif img_go[i,j] == - np.pi/4:
                    delta_i = 1
                    delta_j = -1 
                
                if hessian[i,j] == 0:
                    img_can[i,j] = 1
                elif (hessian[i,j] > 0 and hessian[i+delta_i, j+delta_j] < 0 ) or (hessian[i,j] < 0 and hessian[i+delta_i,j+delta_j] > 0):
                    img_can[i,j] = 1
            
    return img_can
            
            
    
    
           
            
            
            