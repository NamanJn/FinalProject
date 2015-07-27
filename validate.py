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
cap = cv2.VideoCapture("collision2478.mp4")

# initialising the tracker class
print cap.get(3)
print cap.get(4)
print cap.get(5)

ret, frame = cap.read()
#frameROI = frame[ tube_y:tube_y+tube_height, tube_x:tube_x+tube_length ]
#tracker = Tracker(frame, num_of_flies=2)

frame_shape = frame.shape

write_video = False 
if write_video:
    fourcc = cv2.cv.CV_FOURCC('m','p','4','v')
    out = cv2.VideoWriter('output_test.mp4' , fourcc,
        fps=20, frameSize=(frame_shape[0], frame_shape[1]))

while True:

	ret, frame = cap.read()
        cv2.imshow("img", frame)
        cv2.waitKey(500)
	counter +=1
	print counter 

        #frameROI = frame[tube_y:tube_y+tube_height,tube_x:tube_x+tube_length]
        #positions = tracker.apply(frameROI)

        if write_video:
            out.write(frameROI)
            if counter > 500:
                out.release()