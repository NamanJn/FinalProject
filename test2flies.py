import inspect 
import cv2
import pdb
import os
from twoflies import Tracker
import configurations
import sys
ee = execfile

def runTracker(videoNameS, outputdirNameS, tube_x=70, tube_height=23,
               tube_length=500, tube_number=4, y_offset=135, initial_alpha=0.3):

    counter = 0

    # you need to specify this number
    tube_y = y_offset + 42*(tube_number-1)

    # reading the video
    if not os.path.exists(videoNameS):
        print "video does not exist"
        sys.exit()

    cap = cv2.VideoCapture(videoNameS)

    # Initialising the tracker class.
    print cap.get(3)
    print cap.get(4)
    fps = cap.get(5)
    print "frames per second", fps

    if configurations.fps != fps:
        raise ValueError("Change fps in the configuration file!")

    ret, frame = cap.read()
    frameROI = frame[ tube_y:tube_y+tube_height, tube_x:tube_x+tube_length ]

    # initialising the tracker function.
    tracker = Tracker(frameROI, resultsdir=outputdirNameS, writeData=True, writeRawImages=True,
                      writeContourVideo=False, fps=fps, num_of_flies=2, tubeNumber=tube_number,
                      initial_alpha=initial_alpha)

    frame_shape = frameROI.shape
    write_video = False
    if write_video:
        fourcc = cv2.cv.CV_FOURCC('m','p', '4','v')
        out = cv2.VideoWriter('output_test.mp4', fourcc,
            fps=20, frameSize=(frame_shape[0], frame_shape[1]))

    while True:

        ret, frame = cap.read()

        counter +=1
        #print counter

        frameROI = frame[tube_y:tube_y+tube_height,tube_x:tube_x+tube_length]

        positions = tracker.apply(frameROI)

        if write_video:
            out.write(frameROI)
            if counter > 500:
                out.release()


if __name__ == "__main__":

    runTracker('videos/2flies_4hours_10fps.mp4', outputdirNameS='retest_tube4')

