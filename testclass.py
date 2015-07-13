import inspect 
import cv2
import pdb

from myClass import Tracker

ee = execfile

counter = 0
tube_height = 64
tube_length = 550
tube_y = 430
tube_x = 50

# reading the video
cap = cv2.VideoCapture("cut.mp4")

# initialising the tracker class
ret, frame = cap.read()
frame = frame[tube_y:tube_y+tube_height,tube_x:tube_x+tube_length]

tracker = Tracker(frame)

while True:

	ret, frame = cap.read()
        frame = frame[tube_y:tube_y+tube_height,tube_x:tube_x+tube_length]

        positions = tracker.apply(frame)

	print counter 
	counter +=1


