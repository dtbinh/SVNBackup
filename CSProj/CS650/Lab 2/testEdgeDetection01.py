'''
Created on Sep 17, 2014

@author: daqing_yi
'''

from EdgeDetection import *
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img_filename = '2D_White_Box.pgm'
#img_filename = 'blocks.pgm'  
img = Image.open(img_filename).convert("L")
img = np.array(img)

img_laplacian = laplacian(img)

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.imshow(img,cmap = 'gray')
ax1.set_title('Original')
ax1.set_xticks([])
ax1.set_yticks([])

ax2 = fig.add_subplot(122)
ax2.imshow(img_laplacian,cmap = 'gray')
ax2.set_title('Laplacian')
ax2.set_xticks([])
ax2.set_yticks([])

plt.show()