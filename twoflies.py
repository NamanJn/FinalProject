import inspect 
import cv2
import pdb
import numpy as np 
import operator
ee = execfile

class Tracker(object):
    def __init__(self, frame, num_of_flies=1):
        self.frame = frame
        self.gray = cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY)
        self.gray_float = self.gray.astype("float32") 
        self.accumulator = self.gray.astype("float32")
        self.accumulator_int = self.gray.copy()
        self.binary_without_running_average = self.gray.copy()
        self.diff = self.gray.copy() 
        self.binary = self.gray.copy()
        self.previousContour = ["test"]
        self.counter = 0
        self.num_of_flies = num_of_flies

    def getMeanOfContour(contour):
        pass

    def apply(self,frame):
        """
        returns moments (center) of contours
        """
        self.counter += 1
        print self.counter
        self.frame = frame.copy()

	cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY,dst=self.gray)
	#cv2.imshow("gray", self.gray)
        gray_float = self.gray.astype("float32") 

        # drawing the binary threshold image without running average
        cv2.threshold(src=self.gray,
                thresh=80,
                maxval=255,
                type=cv2.THRESH_BINARY_INV,
                dst=self.binary_without_running_average)
         
	#cv2.imshow("threshold without runing average ", self.binary_without_running_average )

        # getting the acummulator average
        cv2.accumulateWeighted(src=gray_float,dst=self.accumulator,alpha=0.001)
        accumulator_int = self.accumulator.astype("uint8")

        #getting the diffs
        cv2.subtract(src1=accumulator_int, src2=self.gray, dst = self.diff)
	#cv2.imshow("diff", self.diff)


        # drawing the binary threshold image with running average
        cv2.threshold(src=self.diff,thresh=30,
                maxval=255,
                type=cv2.THRESH_BINARY,
                dst=self.binary)
        contour = self.binary.copy()
	#cv2.imshow("binary", self.binary)


        # finding the contours 
        contourL, hierarchy = cv2.findContours(image=contour,
                    #mode=cv2.RETR_TREE,
                    mode=cv2.RETR_EXTERNAL,
                    method=cv2.CHAIN_APPROX_SIMPLE)
	#cv2.imshow("contour", contour)
        print "Length of all contours ",len(contourL)


        # drawing all contours 
        allContourFrame = self.frame.copy()
        cv2.drawContours(allContourFrame,contourL,-1,(255,255,0),-1)
        #cv2.imshow("no filtering - all contours shown", allContourFrame)

        # getting big contours  
        bigcontours = [i for i in contourL if cv2.contourArea(i)>30]
        
        # This block is to prevent the losing of the contour
        # need to redo this

        #if len(bigcontours) == 2:
        #    self.previousContour = bigcontours[:]
        #elif len(bigcontours) == 1 and self.previousContour != ["test"]:
        #    bigcontours = self.previousContour[:]

        # drawing the big contours
        bigContourFrame = frame.copy() 
        cv2.drawContours(bigContourFrame, bigcontours,-1,(255,255,0),1)
	#cv2.imshow("1st filter step - big contours", bigContourFrame)


        # getting most squarish looking contour
        # no need for this step if there is only 1 contour.
        # unccoment line below if you want to have the length of the big 
        #if self.counter> 100 and len(bigcontours) > 1:
        if self.counter > 1000:

            squarishcontourL = self.getSquarishContour(bigcontours,draw=False)

            masked = np.zeros(self.gray.shape,np.uint8)     
            cv2.drawContours(masked,bigcontours,-1,(255,255,0),-1)
            pixelpoints = np.transpose(np.nonzero(masked))
            mean_val = cv2.mean(self.gray,mask = masked)
            print "mean_value,", mean_val
            #cv2.imshow("mask", masked) 

            frame_with_square_contour= self.frame.copy()
            cv2.drawContours(frame_with_square_contour, squarishcontourL,-1,(255,255,0),1)
	    #cv2.imshow("2nd filter step - squarish", frame_with_square_contour)

        # printing out the position of the fly
        # getting the moment (to find the center) 
        positions = []
        for i in bigcontours:
            M = cv2.moments(i)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            positions.append([cx,cy])   
        print positions

        # Images to show
        imagesToShowL = [
               self.gray,
               self.diff,
               self.binary,
               allContourFrame,
               bigContourFrame
                ]

        stitched = self.stitchImages(imagesToShowL)

        cv2.imshow("stitched", stitched)
        if cv2.waitKey(5) == ord('a'):
            pdb.set_trace()

        if self.counter %500 == 0 and self.counter> 1: pdb.set_trace()
        if len(bigcontours) == 0 and self.counter > 300: pdb.set_trace()

        return positions 

    def getSquarishContour(self, contourL, draw=False):

        aspect_ratios = []
        contourL = [ i for i in contourL ] # making a deep copy?
        if draw:
            frameCopy = self.frame.copy()
        for cnt in contourL:
            x,y,w,h = cv2.boundingRect(cnt)
            if draw:
                cv2.rectangle(frameCopy,(x,y),(x+w,y+h),(0,255,0),1)
            aspect_ratios.append(abs(float(w)/h -1))

        if draw:
            cv2.imshow("squares", frameCopy)
        min_index, min_value = min(enumerate(aspect_ratios), key=operator.itemgetter(1))
        squarishcontourL = [contourL.pop(min_index)]
        return squarishcontourL 

    def stitchImages(self,frameL):

        if len(frameL[0].shape) == 2:
            stitched = cv2.cvtColor( frameL[0], code = cv2.COLOR_GRAY2BGR )
        elif len(frameL[0].shape) == 3:
            stitched = frameL[0].copy()
        else: 
            print "The images are messed up"

        rest_of_frames = frameL[1:]

        for frame in rest_of_frames:

            converted = frame 
            if len(frame.shape) == 2:
                converted = cv2.cvtColor(frame, code = cv2.COLOR_GRAY2BGR )
            stitched = np.vstack((stitched, converted))

        return stitched

