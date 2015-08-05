import inspect 
import cv2
import pdb
import os
import configurations
import numpy as np
ee = execfile

contour_img_dir = configurations.contour_images_dir
validation_results_dir = configurations.validation_results_dir
results_file = "position_validation.csv"

class ImgListener(object):

    def __init__(self):

        self.positionsL = []
        self.real_positionsL = []
        #self.imageNumber = imageNumber

    def listen_for_click(self,event,x,y,flags,param):
        
        #print param
        if event == cv2.EVENT_LBUTTONUP and len(self.positionsL) < param:
            print x,y
            self.positionsL.append([x,y])
            print "Now positionsL is,", self.positionsL
            coordinates = list(np.array([x,y])/2)
            self.real_positionsL.append(coordinates)
            print "Now positions after halving is,", self.real_positionsL


if __name__ == "__main__":

    frame_interval = 75 
    for i in range(300, 1300, frame_interval):

        img_nameS = "frame%s.png" % i
        print "image is %s" % img_nameS
        frame = cv2.imread(os.path.join(contour_img_dir,img_nameS)    )
        listener = ImgListener()

        # binding listener to the image
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', listener.listen_for_click, param=2)

        # showing the first image and waiting for 2 clicks
        cv2.imshow("image",frame)
        fileToWriteResults = os.path.join(validation_results_dir, results_file)

        print "press 's' to skip to next image"
        print "press 'a' once you are done clicking both flies"
        print "You need to click the number 1 fly first."
        while True:

            aKey = cv2.waitKey(0) 

            if aKey == ord("a") and len(listener.positionsL) == 2:
                for index,positionsL in enumerate(listener.real_positionsL):
                    os.system("echo '%s,fly%s,%s' >> %s" % (i, 
                        index+1,
                        positionsL,
                        fileToWriteResults))
                break
            elif aKey == ord("s"):
                break

