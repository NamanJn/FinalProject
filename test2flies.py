import inspect 
import cv2
import pdb

from twoflies import Tracker

ee = execfile

counter = 0

# you need to specify this number 
tube_number = 4

# tube 9, 
# 1. fly sleeps for time.
# 2. Fly contour gets split into half because the torso is below threshold 

tube_height = 23
tube_length = 500
tube_y = 135 + 42*(tube_number-1)
tube_x = 70

# reading the video
cap = cv2.VideoCapture("2flies.mp4")

# initialising the tracker class
print cap.get(3)
print cap.get(4)

ret, frame = cap.read()
frameROI = frame[ tube_y:tube_y+tube_height, tube_x:tube_x+tube_length ]
tracker = Tracker(frameROI,num_of_flies=2)

while True:

	ret, frame = cap.read()

	counter +=1
	print counter 

        frameROI = frame[tube_y:tube_y+tube_height,tube_x:tube_x+tube_length]
        print frameROI.shape
        #pdb.set_trace()
        positions = tracker.apply(frameROI)






