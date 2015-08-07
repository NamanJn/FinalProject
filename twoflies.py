import inspect 
import cv2
import pdb
import numpy as np 
import operator
import os
ee = execfile

class Tracker(object):
    def __init__(self, frame, num_of_flies=1, tubeNumber = 1):
        self.tubeNumber = tubeNumber 
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
        self.positionsD = {}
        self.previousIsOne = False 
        self.fourcc = None 
        self.out = None 
        self.speed = 7 
        #self.printOut = open("csv.csv","w") 
        self.writing = False
        self.contourVideoName = "output_short_collisions_correct.avi"
        self.collisionLength = 0
        self.contourImgDir = "contour_imgs"
        self.rawImgDir = "raw_imgs"

    def writeAllVideo(self, bigContourFrame):
        if self.counter < 1500:
                if not self.writing:
                    #self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    imageToWrite = self.stitchImages([bigContourFrame])
                    print imageToWrite.shape
                    fourcc = cv2.cv.CV_FOURCC(*'mp4v')
                    pdb.set_trace()
                    self.out = cv2.VideoWriter(self.contourVideoName, fourcc, 25.0, (imageToWrite.shape[1],imageToWrite.shape[0]))
                    self.writing = True;
                else:
                    imageToWrite = self.stitchImages([bigContourFrame])
                    self.out.write(imageToWrite)
        else:
            self.out.release()


    def apply(self,frame):
        """
        returns moments (center) of contours
        """
        self.counter += 1
        print self.counter
        self.frame = frame.copy()

	cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY,dst=self.gray)

        gray_float = self.gray.astype("float32")

        # drawing the binary threshold image without running average
        cv2.threshold(src=self.gray,
                thresh=80,
                maxval=255,
                type=cv2.THRESH_BINARY_INV,
                dst=self.binary_without_running_average)



        # getting the acummulator average
        cv2.accumulateWeighted(src=gray_float,dst=self.accumulator,alpha=0.0005)
        accumulator_int = self.accumulator.astype("uint8")

        #getting the diffs
        cv2.subtract(src1=accumulator_int, src2=self.gray, dst = self.diff)



        # drawing the binary threshold image with running average
        cv2.threshold(src=self.diff,thresh=30,
                maxval=255,
                type=cv2.THRESH_BINARY,
                dst=self.binary)
        contour = self.binary.copy()



        # finding the contours 
        contourL, hierarchy = cv2.findContours(image=contour,
                    #mode=cv2.RETR_TREE,
                    mode=cv2.RETR_EXTERNAL,
                    method=cv2.CHAIN_APPROX_SIMPLE)

        print "Length of all contours ",len(contourL)


        # drawing all contours 
        allContourFrame = self.frame.copy()
        cv2.drawContours(allContourFrame,contourL,-1,(255,255,0),-1)


        # getting big contours  
        bigcontours = []
        contourAreas = []
        for contourItem in contourL:
            contourArea = cv2.contourArea(contourItem)
            print "contourArea is ,", contourArea
            if 30 < contourArea < 700:
                bigcontours.append(contourItem)
                contourAreas.append(contourArea)
        # This block is to prevent the losing of the contour
        # need to redo this

        #if len(bigcontours) == 2:
        #    self.previousContour = bigcontours[:]
        #elif len(bigcontours) == 1 and self.previousContour != ["test"]:
        #    bigcontours = self.previousContour[:]

        # drawing the big contours
        bigContourFrame = frame.copy() 
        cv2.drawContours(bigContourFrame, bigcontours,-1,(255,255,0),1)



        # getting most squarish looking contour
        # no need for this step if there is only 1 contour.
        # unccoment line below if you want to have the length of the big 
        #if self.counter> 100 and len(bigcontours) > 1:
        #if self.counter > 1000:

        #    squarishcontourL = self.getSquarishContour(bigcontours,draw=False)

        #    masked = np.zeros(self.gray.shape,np.uint8)     
        #    cv2.drawContours(masked,bigcontours,-1,(255,255,0),-1)
        #    pixelpoints = np.transpose(np.nonzero(masked))
        #    mean_val = cv2.mean(self.gray,mask = masked)
        #    print "mean_value,", mean_val
        #    #cv2.imshow("mask", masked) 

        #    frame_with_square_contour= self.frame.copy()
        #    cv2.drawContours(frame_with_square_contour, squarishcontourL,-1,(255,255,0),1)
	#    #cv2.imshow("2nd filter step - squarish", frame_with_square_contour)

        # getting the positions of the flies 
        positions = self.getPositions(bigcontours)
        positions_and_areas = []
        for i in zip(positions, contourAreas):
            positions_and_areas.append(i[0],i[1].i[2])

        # conditional block. Testing if 1 or 2 contours found
        positions_proper = {}

        if len(positions) >= 2:

            if self.collisionLength > 10:
                for index, item in enumerate(positions_and_areas):
                    self.positionsD[index+1] = item
                    positions_proper = self.positionsD

            else:
                for fly_id in self.positionsD: 
                    fly_coordinate = self.positionsD[fly_id][:2]
                    distances = [ sum((np.array(fly_coordinate) - np.array(i))**2) for i in positions ]
                    min_index = distances.index(min(distances))
                    positions_proper[fly_id] = positions_and_areas[min_index]
                    print "distances are ", distances
                    print min_index

            #print distances
            rawImg = frame.copy()
            for fly_id, fly_features in positions_proper.iteritems():
                x_coordinate = fly_features[0]
                for image in [bigContourFrame, rawImg]:
                    cv2.putText(image,
                            str(fly_id),
                            (x_coordinate, 18),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.75,
                            (255,255,255))
            print "This is the positions_proper", positions_proper
            self.positionsD = positions_proper
            self.collisionLength = 0

            self.writeRawImagesWithNumbers(self.stitchImages([rawImg]))
        else:
            self.collisionLength += 1


        print positions
        # Images to show.
        if self.counter > 700:
            imagesToShowL = [
                   frame,
                   self.gray,
                   self.diff,
                   self.binary,
                   allContourFrame,
                   bigContourFrame
                    ]
            stitched = self.stitchImages(imagesToShowL)

            # adding key handlers and showign the stiched image
            cv2.imshow("stitched", stitched)
        self.addKeyHandlers()

        self.writeAllVideo(bigContourFrame);

        self.writeDataFile(positions_proper, bigcontours);

        self.writeContourImages(self.stitchImages([bigContourFrame]))



        print '----------------------'
        return positions

    def writeRawImagesWithNumbers(self, image):
        cv2.imwrite(os.path.join(self.rawImgDir,"frame%s.png" % self.counter), image)

    def writeContourImages(self, image):
        cv2.imwrite(os.path.join(self.contourImgDir,"frame%s.png" % self.counter),image) 

    def getPositions(self, bigcontours):
        positions = []
        for i in bigcontours:
            M = cv2.moments(i)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            positions.append([cx,cy])   
        return positions 

    def addKeyHandlers(self):
        if cv2.waitKey(self.speed) == ord('a'):
            pdb.set_trace()
            
        elif cv2.waitKey(self.speed) == ord("f"):
            self.speed = 7

        elif cv2.waitKey(self.speed) == ord("s"):
            self.speed = 100 

    def writeDataFile(self, positions_proper, bigcontours):
            if positions_proper == {}:
                positions_proper = {"1":[[12345,12345],50], "2":[[12345, 12345], 50]}

            if self.counter == 1:
                string = ">"
            elif self.counter > 1:
                string = ">>"
            else:
                raise ValueError("self.counter is less than 1")


            for i in positions_proper:
                coordinatesL = positions_proper[i][:2]
                area = positions_proper[i][2]

                os.system("echo '%s,fly%s,%s,%s,%s' %s data_shortcoll.csv" % (self.counter,
                    i,
                    coordinatesL[0],
                    coordinatesL[1],
                    area,
                    string))

            os.system("echo %s %s csv.csv" % (len(bigcontours),string))

        
    # this function is broken. don't use it
    def writeSingleContourVideos(self):
        if self.counter < 600 and len(bigcontours) ==1:
            if not self.previousIsOne:
                #self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
                imageToWrite = self.stitchImages([bigContourFrame])
                print imageToWrite.shape
                fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
                self.out = cv2.VideoWriter('output%s.mp4' % self.counter ,
                        fourcc, 25.0, (imageToWrite.shape[0],imageToWrite.shape[1]))
                #cv2.imwrite("image%s.png" % self.counter, self.stitchImages([bigContourFrame]))
                self.out.write(imageToWrite)
                self.previousIsOne = True
            else:
                self.out.write(bigContourFrame)
                print "Writing now"
                pdb.set_trace() 
        else:
            if self.previousIsOne:
                self.out.release() 
                self.previousIsOne = False


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
            raise ValueError("The images are neither are 3 or 2 dimensional") 

        rest_of_frames = frameL[1:]

        for frame in rest_of_frames:

            converted = frame 
            if len(frame.shape) == 2:
                converted = cv2.cvtColor(frame, code = cv2.COLOR_GRAY2BGR )
            stitched = np.vstack((stitched, converted))

        stitched_double = cv2.resize(stitched, dsize=None,
                fx=2,
                fy=2,
                interpolation = cv2.INTER_CUBIC)
        return stitched_double

