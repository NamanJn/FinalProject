
import inspect 
import cv2
import pdb

ee = execfile


cap = cv2.VideoCapture("cut.mp4")
ret, frame = cap.read()
counter = 0
gray = cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY)
gray_float  = gray.astype("float32")
accumulator = gray.astype("float32")
accumulator_int = gray.copy()
diff = gray.copy()
binary = gray.copy()
#pdb.set_trace()
while True:

	ret, frame = cap.read()
	cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY,dst=gray)
        pdb.set_trace()
	#gray = cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY)
        gray_float = gray.astype("float32") 

        cv2.accumulateWeighted(src=gray_float,dst=accumulator,alpha=0.01)
        accumulator_int = accumulator.astype("uint8")
        
        # finding diff between running average and current
        cv2.absdiff(src1=accumulator_int, src2=gray,dst=diff)
        
        # doing adaptive threshold
        cv2.adaptiveThreshold(src=diff,maxValue=255,
               adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
               thresholdType=cv2.THRESH_BINARY,
               blockSize = 21,
               C = 5,
               dst = binary)
        ##cv2.threshold(src=diff,thresh=20,
        #        maxval=255,
        #        type=cv2.THRESH_BINARY,
        #        dst=binary)


        # finding the contours 
        contour = binary.copy()
        contourL, hierarchy = cv2.findContours(image=contour,
                    mode=cv2.RETR_TREE,
                    method=cv2.CHAIN_APPROX_SIMPLE)

        #drawcontour = binary.copy() 
        cv2.drawContours(frame, contourL,0,(0,255,0),3)

	#cv2.imshow("img",accumulator_int)
	cv2.imshow("img",contour)

        if counter == 500:
            pdb.set_trace()
            cv2.findContours(image=binary,
                    mode=cv2.RETR_TREE,
                    method=cv2.CHAIN_APPROX_SIMPLE)
	cv2.waitKey(1)
	print counter 
	counter +=1
