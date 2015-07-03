import inspect 
import cv2
import pdb

ee = execfile

counter = 0

tube_height = 64
tube_length = 550

tube_y = 430
tube_x = 50

cap = cv2.VideoCapture("cut.mp4")
ret, frame = cap.read()
frame = frame[tube_y:tube_y+tube_height,tube_x:tube_x+tube_length]


gray = cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY)
gray_float  = gray.astype("float32")
accumulator = gray.astype("float32")
accumulator_int = gray.copy()
diff = gray.copy()
binary = gray.copy()
#pdb.set_trace()
while True:

	ret, frame = cap.read()
        frame = frame[tube_y:tube_y+tube_height,tube_x:tube_x+tube_length]
        #for i in range(10):
        #    cv2.rectangle(frame,(50,170+i*(tube_height)),(550,170+(i+1)*tube_height),(0,255,0),3)
        # gray scaling the image
	cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY,dst=gray)
        gray_float = gray.astype("float32") 

        # doing the running average
        cv2.accumulateWeighted(src=gray_float,dst=accumulator,alpha=0.001)
        accumulator_int = accumulator.astype("uint8")
        
        # finding diff between running average and current
        #cv2.absdiff(src1=accumulator_int, src2=gray,dst=diff)
        cv2.subtract(src1=accumulator_int, src2=gray,dst=diff)
                 
	cv2.imshow("diff", diff)
        # doing adaptive threshold
        #cv2.adaptiveThreshold(src=diff,maxValue=255,
        #       adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #       thresholdType=cv2.THRESH_BINARY_INV,
        #       blockSize = 201,
        #       C = 0,
        #       dst = binary)
        
        cv2.threshold(src=diff,thresh=20,
                maxval=255,
                type=cv2.THRESH_BINARY,
                dst=binary)

        # finding the contours 
        contour = binary.copy()
	cv2.imshow("binary", binary)
        contourL, hierarchy = cv2.findContours(image=contour,
                    #mode=cv2.RETR_TREE,
                    mode=cv2.RETR_EXTERNAL,
                    method=cv2.CHAIN_APPROX_SIMPLE)
	cv2.imshow("contour", contour)
        print len(contourL)

        # getting big contours  
        bigcontours = [i for i in contourL if cv2.contourArea(i)>50]
        
        # printing out the position of the fly
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
	print counter 
	counter +=1
