import inspect 
import cv2
import pdb

# This script's aim is to get input from a user
# whether the tracking system switched the identity or no
# Ths userinput will just be "yes" or "no".
# If yes, then switch the identities downstream of the collision.
# If no, then nothing is changed downstream. 

from twoflies import Tracker

ee = execfile

counter = 0

# reading the video
cap = cv2.VideoCapture("collision2478.mp4")

# initialising the tracker class
print cap.get(3)
print cap.get(4)
print cap.get(5)

ret, frame = cap.read()
#frameROI = frame[ tube_y:tube_y+tube_height, tube_x:tube_x+tube_length ]
#tracker = Tracker(frame, num_of_flies=2)

# listener function
#positionsL = []
#def draw_circle(event,x,y,flags,param):
#    global cv2,frame,positionsL
#    print param
#    if event == cv2.EVENT_LBUTTONUP and len(positionsL) < param:
#        print x,y
#        positionsL.append([x,y])
#        print "Now positionsL is,", positionsL
#
## binding listener to the image
#cv2.namedWindow('image')
#cv2.setMouseCallback('image', draw_circle, param=2)

# showing the first image and waiting for 2 clicks
cv2.imshow("image",frame)
while True:
    aKey = cv2.waitKey(0) 
    if aKey == ord("a"):
        break


frame_shape = frame.shape
write_video = False 
if write_video:
    fourcc = cv2.cv.CV_FOURCC('m','p','4','v')
    out = cv2.VideoWriter('output_test.mp4' , fourcc,
        fps=20, frameSize=(frame_shape[0], frame_shape[1]))

while True:
        breakloop = False

        cv2.waitKey(100)
	ret, frame = cap.read()
        
        if not ret:
            cv2.setMouseCallback('image', draw_circle, param=4)
            print positionsL
            while True:
                aKey = cv2.waitKey(0) 
                if aKey == ord("a") and len(positionsL) ==4:
                    breakloop = True
                    break
                         
        if breakloop:
            break

        cv2.imshow("image", frame)
	counter +=1
	#print counter 

        #frameROI = frame[tube_y:tube_y+tube_height,tube_x:tube_x+tube_length]
        #positions = tracker.apply(frameROI)

        if write_video:
            out.write(frameROI)
            if counter > 500:
                out.release()
