import os
import os.path
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from keras.models import Sequential,load_model
from PIL import Image
import keras,sys
import numpy as np
import cv2 as cv
import argparse
import random


# Initialize the parameters
confThreshold = 0.5  # Confidence threshold
maskThreshold = 0.3  # Mask threshold

parser = argparse.ArgumentParser(description='Use this script to run Mask-RCNN object detection and segmentation')
parser.add_argument('--image', help='Path to image file')
parser.add_argument('--video', help='Path to video file.')
parser.add_argument("--device", default="cpu", help="Device to inference on")
args = parser.parse_args()

def imgClassification(frame, score, classId, classMask):
    # Print a label of class.
    print('-' * 50)
    label = '%.2f' % (score * 100) + '%'
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label) #ここですわ
        print(label)

        ex_classesFile = "explanation.txt";
        ex_classes = None
        with open(ex_classesFile, 'rt') as f:
            ex_classes = f.read().rstrip('\n').split('\n')
        print(ex_classes[classId])

    print('-' * 50)
    

# For each frame, extract the bounding box and mask for each detected object
def postprocess(boxes, masks):
    numClasses = masks.shape[1]
    numDetections = boxes.shape[2]
    frameH = frame.shape[0]
    frameW = frame.shape[1]
    
    for i in range(numDetections):
        box = boxes[0, 0, i]
        mask = masks[i]
        score = box[2]
        if score > confThreshold:
            classId = int(box[1])
            
            # Extract the mask for the object
            classMask = mask[classId]

            imgClassification(frame, score, classId, classMask)


# Load names of classes
classesFile = "mscoco_labels.names"
classes = None
with open(classesFile, 'rt') as f:
   classes = f.read().rstrip('\n').split('\n')

# Give the textGraph and weight files for the model
textGraph = "./AWS_ASDI_EcoProject.pbtxt"
modelWeights = "./AWS_ASDI_EcoProject/frozen_inference_graph.pb"


# Load the network
net = cv.dnn.readNetFromTensorflow(modelWeights, textGraph);
if args.device == "cpu":
    net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)
elif args.device == "gpu":
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)


# Load the classes
colorsFile = "colors.txt";
with open(colorsFile, 'rt') as f:
    colorsStr = f.read().rstrip('\n').split('\n')
colors = [] #[0,0,0]
for i in range(len(colorsStr)):
    rgb = colorsStr[i].split(' ')
    color = np.array([float(rgb[0]), float(rgb[1]), float(rgb[2])])
    colors.append(color)


winName = 'AWS-ASDI Eco Project'
cv.namedWindow(winName, cv.WINDOW_NORMAL)


outputFile = "_AWS_ASDI.jpg"
if (args.image):
    # Open the image file
    if not os.path.isfile(args.image):
        print("Input image file ", args.image, " doesn't exist")
        sys.exit(1)
    cap = cv.VideoCapture(args.image)
    outputFile = args.image[:-4]+'_AWS_ASDI.jpg'
elif (args.video):
    # Open the video file
    if not os.path.isfile(args.video):
        print("Input video file ", args.video, " doesn't exist")
        sys.exit(1)
    cap = cv.VideoCapture(args.video)
    outputFile = args.video[:-4]+'_AWS_ASDI.avi'
else:
    print("No input is detected")


hasFrame, frame = cap.read()
blob = cv.dnn.blobFromImage(frame, swapRB=True, crop=False)
net.setInput(blob)
boxes, masks = net.forward(['detection_out_final', 'detection_masks'])
postprocess(boxes, masks)