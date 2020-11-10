import numpy as np
import cv2
# import os
# from tabulate import tabulate
import classifier
from PIL import Image
from kafka import KafkaConsumer
from json import loads
import pickle
import logging
import time


def car_rec(image,confidence=0.5,threshold=0.3):

   car_color_classifier = classifier.Classifier()

   labelsPath = ("coco.names")
   weightsPath = ("yolov3.weights")
   configPath = ("yolov3.cfg")
   LABELS = open(labelsPath).read().strip().split("\n")

   # load our YOLO object detector trained on COCO dataset (80 classes)
   net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

   # load our input image and grab its spatial dimensions

   (H, W) = image.shape[:2]

   # determine only the output layer names that we need from YOLO
   layer_names = net.getLayerNames()
   output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


   # construct a blob from the input image and then perform a forward
   # pass of the YOLO object detector, giving us our bounding boxes and
   # associated probabilities

   blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
   net.setInput(blob)
   outputs = net.forward(output_layers)


   # initialize our lists of detected bounding boxes, confidences, and
   # class IDs, results,  respectively
   boxes = []
   confidences = []
   classIDs = []
   results = []


   # loop over each of the layer outputs
   for output in outputs:

      # loop over each of the detections
      for detection in output:

         # extract the class ID and confidence (i.e., probability) of
         # the current object detection
         scores = detection[5:]
         classID = np.argmax(scores)
         confident = scores[classID]

         # filter out weak predictions by ensuring the detected
         # probability is greater than the minimum probability
         if confident > confidence:

            # scale the bounding box coordinates back relative to the            
            # size of the image, keeping in mind that YOLO actually
            # returns the center (x, y)-coordinates of the bounding
            # box followed by the boxes' width and height
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY, width, height) = box.astype("int")


            # use the center (x, y)-coordinates to derive the top and
            # and left corner of the bounding box
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))


            # update our list of bounding box coordinates, confidences,
            # and class IDs
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confident))
            classIDs.append(classID)

   
   # apply non-maxima suppression to suppress weak, overlapping bounding boxes
   idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence, threshold)

   # ensure at least one detection exists
   if len(idxs) > 0:
      # loop over the indexes we are keeping
      for i in idxs.flatten():

         # extract the bounding box coordinates
         (x, y) = (boxes[i][0], boxes[i][1])
         (w, h) = (boxes[i][2], boxes[i][3])


         if classIDs[i] == 2:

	    # x,y,w,h, auto, marka, model
            result = car_color_classifier.predict(image[max(y,0):y + h, max(x,0):x + w])
            results.append([x,y,w,h,LABELS[classIDs[i]],result[0]['make'],result[0]['model']])
         else:
	    # x,y,w,h, rodzaj przedmiotu
            results.append([x,y,w,h,LABELS[classIDs[i]]])

   # save results in results.txt
   #with open('results.txt', 'w') as f:
   #   f.write(tabulate(results))

   #print(tabulate(results))

   return(results)

consumer = KafkaConsumer(
    'topic_test',
    bootstrap_servers=['kafka:9093'],
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

for event in consumer:
   data = event.value
   timestamp, image = pickle.loads(data)
   print(car_rec(image))