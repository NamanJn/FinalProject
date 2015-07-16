import inspect 
import cv2
import pdb

from myClass import Tracker

ee = execfile

counter = 0

# you need to specify this number 
tube_number = 3

# tube 9, 
# 1. fly sleeps for time.
# 2. Fly contour gets split into half because the torso is below threshold 

tube_height = 50
tube_length = 550
tube_y = 170 + 65*(tube_number-1)
tube_x = 50

# reading the video
cap = cv2.VideoCapture("cut.mp4")

# initialising the tracker class

ret, frame = cap.read()
frameROI = frame[tube_y:tube_y+tube_height,tube_x:tube_x+tube_length]
tracker = Tracker(frameROI)

while True:

	ret, frame = cap.read()
        cv2.imshow("all", frame)
        cv2.waitKey(1)
        frameROI = frame[tube_y:tube_y+tube_height,tube_x:tube_x+tube_length]

        positions = tracker.apply(frameROI)

	print counter 
	counter +=1


