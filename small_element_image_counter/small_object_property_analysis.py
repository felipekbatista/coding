"""
Created on Thu Apr 30 15:48:35 2020
modified in aug 7th 2021
@author: das_fox
version 1.0

measure properties in multiple images and yield geometric information.
good for counting multiples objects such as salt grains, beans, rice, rocks


there are example images in the directory_example.
- 4 pictures of salt grains
- 1 picture of coins
these pictures show the kind of imgs that can be used for this program


input: 
    - images path
        imgs must be .jpg format
    - csv filename
        name the csv output file
    
output: csv file
    - area [pixel^2]
    - labels [number ID]
    - perimeter [pixel]
    - major axis length [pixel]
    - minor axis length [pixel]
    - equivalent diameter [pixel]
"""

#libraries import
from matplotlib import pyplot as plt
from skimage import io, img_as_ubyte, measure
import glob
import numpy as np
from scipy import ndimage
import cv2
import pandas as pd
import os

print('program start')
print('if imgs are in the same directory as the code, simply hit enter')
img_path = input('image path: ')
img_path_jpg = os.path.join(img_path, '*.jpg' )
print('image path acquired')

print('\n --- \n')

print('csv filename ')
csv_filename = input('csv filename: ')
print('csv filename acquired')
print(' \n --- \n')


print('lists creation')
list_area=['area']
list_labels=['labels']
list_perimeter = ['perimeter']
list_majax = ['major axis']
list_minax = ['minor axis']
list_eqdiam =['eqv diameter']
        
list_all = [list_labels, 
                list_area,
                list_perimeter,
                list_majax,
                list_minax,
                list_eqdiam]

#path = '\*.jpg'
index = 0
pathlist = []
for file in glob.glob(img_path_jpg):
    print('reading')
    #img1 = io.imread(path, as_gray = False)
    print(file)
    print(index)
    img2 = img_as_ubyte(io.imread(file, as_gray = True))
    img_clr = io.imread(file, as_gray = False)
    plt.imshow(img2, cmap = 'gray')
    index += 1    
    
    print('threshold')
    #threshold the img
    ret, thresh = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU )
    io.imshow(thresh)
    
    print('bordercleaning')
    #border clearing 
    from skimage.segmentation import clear_border
    thresh_brdclr = clear_border(thresh)
    io.imshow(thresh_brdclr, cmap = 'gray')
    
    print('opening')
    #opening to eliminate the noisy background
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(thresh_brdclr,kernel,iterations = 2)
    dilation = cv2.dilate(erosion,kernel,iterations = 2)
    #erosion = cv2.erode(dilation,kernel,iterations = 1)
    #dilation = cv2.dilate(erosion,kernel,iterations = 1)
    
    
    #opening = cv2.morphologyEx(thresh_brdclr, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
    #io.imshow(dilation, cmap = 'gray')
    
    print('sure background')
    #sure bg area
    sure_bg = cv2.dilate(dilation, kernel, iterations = 3)
    
    print('sure foreground')
    #sure foreground area
    dist_transform = cv2.distanceTransform(dilation, cv2.DIST_L2, 5)
    ret2, sure_fg = cv2.threshold(dist_transform, 0.2*dist_transform.max(), 255,0)
    #plt.imshow(sure_fg, cmap = 'gray')
    
    
    print('unknown')
    #unknow region - simply subtract the images
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    #plt.imshow(unknown, cmap = 'jet')
    
    print('marker')
    #marker labeling - set labels 2 fg objects
    ret3, markers = cv2.connectedComponents(sure_fg)
    #add 1 to all labels, so to make sure background is not 0, but 1 (differentiate from unknown)
    markers = markers + 1
    
    print('marker update')
    #mark the unknown region with zero 
    markers[unknown == 255] = 0
    #it uses the previous unknown region as a mask for updating the marker
    
    #final step - apply watershd
    #markers = cv2.watershed(img2, markers)
    #from skimage.morphology import watershed
    
    from skimage.segmentation import watershed
    print('watershed implementation')
    markers = watershed(dist_transform, 
                        mask = img2 )
    #markers = watershed(-dist_transform, markers, mask = img2)
    #plt.imshow(markers, cmap = 'jet')
    img_clr[markers == 1] = [0,255,0]
    
    #information extract
    regions = measure.regionprops(markers, intensity_image = None)
    #element = 0
    #region_length = len(regions)
    print('loop front')
    for i,element in enumerate(regions): #need to set the upper limit to list length
        print('inside loop - begin')
        print(regions[i].area)
        list_area.append(regions[i].area)
        list_labels.append(regions[i].label)
        list_perimeter.append(regions[i].perimeter)
        list_majax.append(regions[i].major_axis_length)
        list_minax.append(regions[i].minor_axis_length)
        list_eqdiam.append(regions[i].equivalent_diameter)
        print('inside loop - end')

print('outside loop')
listall = np.array(list_all)

listallT = np.transpose(listall)

dataframe1 = pd.DataFrame(listallT)
csv_filename_path = os.path.join(csv_filename, '.csv')
dataframe1.to_csv(csv_filename + '.csv' , sep = ';')

print('process finished')
print('check for the csv file')

    


