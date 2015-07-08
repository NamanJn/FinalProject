import inspect 
import cv2
import pdb

ee = execfile

class Tracker(object):
    def __init__(self,frame):
        self.gray = cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY)
        self.gray_float = self.gray.astype("float32") 
        self.accumulator = self.gray.astype("float32")
        self.accumulator_int = self.gray.copy()
        self.diff = self.gray.copy() 
        self.binary = self.gray.copy()
        self.previousContour = ["test"]

    def apply(self,frame):
        """
        returns moments (center) of contours
        """
	    cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY,dst=self.gray)
        gray_float = self.gray.astype("float32") 

        cv2.accumulateWeighted(src=gray_float,dst=self.accumulator,alpha=0.001)
        accumulator_int = self.accumulator.astype("uint8")

        cv2.subtract(src1=accumulator_int, src2=self.gray, dst = self.diff)
	cv2.imshow("diff", self.diff)


        cv2.threshold(src=self.diff,thresh=20,
                maxval=255,
                type=cv2.THRESH_BINARY,
                dst=self.binary)

         # finding the contours 
        contour = self.binary.copy()
	cv2.imshow("binary", self.binary)
        contourL, hierarchy = cv2.findContours(image=contour,
                    #mode=cv2.RETR_TREE,
                    mode=cv2.RETR_EXTERNAL,
                    method=cv2.CHAIN_APPROX_SIMPLE)

	cv2.imshow("contour", contour)
        print len(contourL)

        # getting big contours  
        bigcontours = [i for i in contourL if cv2.contourArea(i)>50]

        #pdb.set_trace()
        # This block is to prevent the losing of the contour
        if len(bigcontours) == 1:
            self.previousContour = bigcontours[:]
        elif len(bigcontours) == 0 and self.previousContour != ["test"]:
            bigcontours = self.previousContour[:]

        # printing out the position of the fly
        # getting the moment (to find the center) 
        positions = []
        for i in bigcontours:
            M = cv2.moments(i)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            positions.append([cx,cy])   
        print positions

        cv2.drawContours(frame, bigcontours,-1,(255,255,0),1)

	cv2.imshow("img", frame)

	cv2.waitKey(10)
        return positions 
