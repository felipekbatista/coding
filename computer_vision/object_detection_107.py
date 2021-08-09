# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 12:17:03 2021

@author: das_fox
master local directory: object_detection_107
"""

# download darknet files 
'''
!git clone https://github.com/pjreddie/darknet
cd darknet - use this for a GPU
'''
#download the pre-trained weight file 
'''
I could not use the wget and git clone commands to download, so I used the 
download link provided in the webpage of yolov3
'''
'''
import wget
wget https://pjreddie.com/media/files/yolov3.weights
!git clone https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg

# coco.names downloaded
'link for download: https://gitlab.com/EAVISE/darknet/blob/master/data/coco.names'
'''
import cv2 
import numpy as np

#pathes used for the dnn.readnet
'file config and weights - use this for various tipes needs: high acc our high speed'

yolo_cfg = 'darknet/cfg/yolov3.cfg'
yolo_weights = 'yolov3.weights'
net = cv2.dnn.readNet(yolo_weights, yolo_cfg)

#create classes of the object detector
'create the classes for the objects detected in imgs using the coco.names'

classes = []
coco_names = 'coco.names'
with open(coco_names, 'r') as f:
    classes = f.read().splitlines()
print(classes)

# input selection
'choose between a static img or video or live cam'

img_path = ['imagens/airplane.jpg', 'imagens/bike.jpg',
            'imagens/clock.jpg', 'imagens/dog.jpg', 
            'imagens/person_bike.jpg','imagens/watch.jpg']
i = 5

#img = cv2.imread(img_path[i])
'use this bellow for livecam or a video'

cap = cv2.VideoCapture(0)

while True:  #use this loop only for a video
    
    ret, img = cap.read()        
    height, width, _ = img.shape
    
    #create the input of the img to pass it to the net object
    blob = cv2.dnn.blobFromImage(img, 1 / 255 , (416,416),(0,0,0), swapRB = True, crop = False)
    
    net.setInput(blob)
    output_layers_name = net.getUnconnectedOutLayersNames()
    layerOutput = net.forward(output_layers_name)
    
    boxes = []
    confidences = []
    class_ids = []
    
    threshold = 0.5
    
    for output in layerOutput:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                boxes.append( [ x, y, w, h])
                confidences.append( (float(confidence)))
                class_ids.append(class_id)
    
    print('',len(boxes))
    #Non Maximum Suppression: keeps only the high score box
    indexes = cv2.dnn.NMSBoxes(bboxes = boxes, 
                               scores = confidences, 
                               score_threshold = threshold , 
                               nms_threshold = 0.4) #supresses NonMaximum Scores
    print('indexes flatened' )#,indexes.flatten())
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    colors = np.random.uniform( 0, 255, size = ( len( boxes), 3))
    
    for i in indexes.flatten():
        x, y, w, h = boxes[i] # box vertices locations
        label = str( classes[class_ids[i]]) #extract the name from the classes
        confidence = str( round(confidences[i], 2)) #confidence interval that will be shown in the picture
        color = colors[i]
        cv2.rectangle( img, (x, y), ( x + w, y + h), color, 2)
        cv2.putText(img, label + ' ' + confidence, 
                    ( x , y + 20), 
                    fontFace = font , 
                    fontScale = 1,
                    color = (0,200,0),
                    thickness = 2) 
    
    
    cv2.imshow('pessoa e bike', img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

