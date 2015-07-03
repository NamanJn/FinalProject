
import inspect 
import cv2
import pdb

ee = execfile


counter = 0
cap = cv2.VideoCapture("cut.mp4")
ret, frame = cap.read()
#frame = frame[100:225,50:550]


gray = cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY)
gray_float  = gray.astype("float32")
accumulator = gray.astype("float32")
accumulator_int = gray.copy()
diff = gray.copy()
binary = gray.copy()
#pdb.set_trace()
while True:

	ret, frame = cap.read()
        #frame = frame[100:225,50:550]
	cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY,dst=gray)
        #roi = frame.copy()[100:250,50:550]
        #pdb.set_trace()
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
               blockSize = 11,
               C = 3,
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
        bigcontours = [i for i in contourL if cv2.contourArea(i)>150]
        try:
            cv2.drawContours(frame, bigcontours,-1,(255,255,0),2)
        except:
            pass
	#cv2.imshow("img",accumulator_int)
	cv2.imshow("img", binary)

        if counter == 500:
            pdb.set_trace()
            cv2.findContours(image=binary,
                    mode=cv2.RETR_TREE,
                    method=cv2.CHAIN_APPROX_SIMPLE)
	cv2.waitKey(10)
	print counter 
	counter +=1
