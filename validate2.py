import inspect 
import cv2
import pdb
import os
# This script's aim is to get input from a user
# whether the tracking system switched the identity or no
# Ths userinput will just be "yes" or "no".
# If yes, then switch the identities downstream of the collision.
# If no, then nothing is changed downstream. 

from twoflies import Tracker

ee = execfile


videoDirS = "collision_vids"
videosL = os.listdir(videoDirS)

def playVideo(videoNameS):

    counter = 0
    cap = cv2.VideoCapture(os.path.join(videoDirS,videoS))
    ret, frame = cap.read()
    cv2.imshow("image",frame)
    while True:
        aKey = cv2.waitKey(0) 
        if aKey == ord("a"):
            break


    frame_shape = frame.shape
    write_video = False 

    while True:
            breakloop = False

            cv2.waitKey(100)
            ret, frame = cap.read()
            
            if not ret:
                while True:
                    aKey = cv2.waitKey(0) 
                    if aKey == ord("a"):
                        breakloop = True
                        break
                             
            if breakloop:
                break

            cv2.imshow("image", frame)
            counter += 1
     
for videoS in videosL:
    # reading the video
    #collisionFrame = 916 
    #cap = cv2.VideoCapture("collision_vids/collision%s_withcontours.mp4" % collisionFrame)
    pdb.set_trace()    
    playVideo(os.path.join(videoDirS, videoS))

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

    while True:
        x = raw_input("Did identities switch? [y/n/r]: ")
        if x == "y":
            print "ok switched"
            break
        elif x == "n":
            print "ok didn't switch"
            break
        elif x == "r":
            print "playing again"
            playVideo(os.path.join(videoDirS, videoS))
        else:
            print "try again"

print "finished!"
