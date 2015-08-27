import inspect 
import cv2
import pdb
import numpy as np 
import operator
import os
import configurations
ee = execfile
import operator

class Tracker(object):
    def __init__(self, frame, tubeNumber, fps, resultsdir,
                 writeData=False, writeContourVideo=False,
                 writeRawImages=False, writeContourImages = False,
                 num_of_flies=1):

        self.tubeNumber = tubeNumber
        self.frame = frame
        self.gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
        self.gray_float = self.gray.astype("float32") 
        self.accumulator = self.gray.astype("float32")
        self.accumulator_int = self.gray.copy()
        self.binary_without_running_average = self.gray.copy()
        self.diff = self.gray.copy() 
        self.binary = self.gray.copy()
        self.previousContour = ["test"]
        self.counter = 0
        self.fps = fps
        self.num_of_flies = num_of_flies
        self.positionsD = {}
        self.previousIsOne = False 
        self.fourcc = None
        self.out = None 
        self.speed = 2
        self.writeData = writeData
        self.writeContourVideo = writeContourVideo
        self.writing = False
        self.contourVideoName = "output_multipleframes.avi"
        self.collisionLength = 0


        self.maxFlyGrayScaleValue = 117
        self.alpha = 0.3

        self.writeRawImages = writeRawImages
        self.writeContourImages = writeContourImages
        self.contourArea_lowerBound = 30

        # directories and paths ( Directories have to end with '[Dd]ir')
        self.results_dir = resultsdir
        self.debug_imgs_dir = os.path.join(self.results_dir, configurations.debug_images_dir)
        self.data_dir = os.path.join(self.results_dir, configurations.data_dir)
        self.rawImgDir = os.path.join(self.results_dir, configurations.raw_imgs_dir)
        self.contourImgDir = os.path.join(self.results_dir, "contour_imgs")

        # creating the directories
        self.createDirectories()

        # file paths
        self.dataFilePathS = os.path.join(self.data_dir, "data.csv")
        self.test_rleFilePathS = os.path.join(self.results_dir, configurations.rle_data_file)

    def writeAllVideo(self, framesL):
        if self.counter < 100000:

                imageToWrite = self.stitchImages(framesL)
                if not self.writing:
                    #self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

                    print imageToWrite.shape
                    fourcc = cv2.cv.CV_FOURCC(*'mp4v')
                    pdb.set_trace()
                    self.out = cv2.VideoWriter(self.contourVideoName, fourcc, self.fps, (imageToWrite.shape[1], imageToWrite.shape[0]))
                    self.writing = True
                else:

                    self.out.write(imageToWrite)
        else:
            self.out.release()

    def createDirectories(self):
        """
        This creates the appropriate directories needed to save the results.
        """

        # This gets the names of the directories
        directoriesL = [self.__dict__[i] for i in self.__dict__.keys() if (i.endswith("dir") or i.endswith("Dir"))]

        for directoryS in directoriesL:
            if not os.path.exists(directoryS):
                os.makedirs(directoryS)

    def apply(self, frame):
        """
        returns moments (center) of contours
        """
        self.counter += 1
        if self.counter % 500 == 0: print self.counter
        if self.counter == 3000:
            self.maxFlyGrayScaleValue = 130
            self.contourArea_lowerBound = 20

        self.frame = frame.copy()

        # converting frame to grayscale
        cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY, dst=self.gray)
        gray_float = self.gray.astype("float32")

        # drawing the binary threshold image without running average
        # cv2.threshold(src=self.gray,
        #         thresh=80,
        #         maxval=255,
        #         type=cv2.THRESH_BINARY_INV,
        #         dst=self.binary_without_running_average)

        # getting the acumulator average

        self.alpha -= 0.001
        if self.alpha < 0:
            self.alpha = 0.0
        else:
            print self.alpha

        cv2.accumulateWeighted(src=gray_float, dst=self.accumulator, alpha=self.alpha)
        accumulator_int = self.accumulator.astype("uint8")

        #getting the diffs
        cv2.subtract(src1=accumulator_int, src2=self.gray, dst=self.diff)



        # drawing the binary threshold image with running average
        cv2.threshold(src=self.diff,thresh=20,
                maxval=255,
                type=cv2.THRESH_BINARY,
                dst=self.binary)
        contour = self.binary.copy()



        # finding the contours 
        contourL, hierarchy = cv2.findContours(image=contour,
                    #mode=cv2.RETR_TREE,
                    mode=cv2.RETR_EXTERNAL,
                    method=cv2.CHAIN_APPROX_SIMPLE)

        #print "Length of all contours ",len(contourL)


        # drawing all contours 
        allContourFrame = self.frame.copy()
        cv2.drawContours(allContourFrame,contourL,-1,(255,255,0),-1)


        # getting big contours  
        bigcontours = []
        contourAreas = []
        for contourItem in contourL:
            contourArea = cv2.contourArea(contourItem)
            #print "contourArea is ,", contourArea
            if self.contourArea_lowerBound < contourArea < 700:
                bigcontours.append(contourItem)
                contourAreas.append(contourArea)
        bigContourFrame = frame.copy()
        cv2.drawContours(bigContourFrame, bigcontours,-1,(255,255,0),1)
        # This block is to prevent the losing of the contour
        # need to redo this

        #if len(bigcontours) == 2:
        #    self.previousContour = bigcontours[:]
        #elif len(bigcontours) == 1 and self.previousContour != ["test"]:
        #    bigcontours = self.previousContour[:]

        # drawing the big contours


        mean_valuesL, maskedL, fly_mean_and_contour_and_contourAreas = self.getOnlyFlyContourAndMean(bigcontours, contourAreas)

        #nonBackgroundContourL


        #print "mean_value,", mean_val

        # getting most squarish looking contour
        # no need for this step if there is only 1 contour.
        # unccoment line below if you want to have the length of the big 
        #if self.counter> 100 and len(bigcontours) > 1:
        #if self.counter > 1000:

        #    squarishcontourL = self.getSquarishContour(bigcontours,draw=False)

        #    frame_with_square_contour= self.frame.copy()
        #    cv2.drawContours(frame_with_square_contour, squarishcontourL,-1,(255,255,0),1)
	    #cv2.imshow("2nd filter step - squarish", frame_with_square_contour)

        # getting the positions of the flies

        bigAndFlyContours = [ i[1] for i in fly_mean_and_contour_and_contourAreas]
        bigAndFlyContourAreas = [ i[2] for i in fly_mean_and_contour_and_contourAreas]
        bigAndFlyMean = [ i[0][0] for i in fly_mean_and_contour_and_contourAreas]

        bigAndOnlyFlyContourFrame = frame.copy()
        cv2.drawContours(bigAndOnlyFlyContourFrame, bigAndFlyContours,-1,(255,255,0),1)

        # getting width of contours
        boundingRectFrame = bigAndOnlyFlyContourFrame.copy()
        widthsL = [50]
        if len(bigAndFlyContours) >= 2:
            #print len(bigAndFlyContours)
            boundingRectFrame, widthsL = self.getWidthOfContours(bigAndFlyContours, bigAndOnlyFlyContourFrame)


        positions = self.getPositions(bigAndFlyContours)
        positions_and_areas = []
        for i in zip(positions, bigAndFlyContourAreas, bigAndFlyMean,widthsL):
            positions_and_areas.append((i[0][0], i[0][1], i[1], i[2], i[3]))

        # conditional block. Testing if 1 or 2 contours found
        positions_proper = {}

        if len(positions) >= 2:
            if self.collisionLength > self.fps * 0.4:
                for index, item in enumerate(positions_and_areas):
                    self.positionsD[index+1] = item
                positions_proper = self.positionsD

            else:
                distancesL = []
                firstIndex= None
                for fly_id in self.positionsD: 
                    fly_coordinate = self.positionsD[fly_id][:2]
                    distances = [ sum((np.array(fly_coordinate) - np.array(i))**2) for i in positions ]
                    min_index = distances.index(min(distances))
                    positions_proper[fly_id] = positions_and_areas[min_index]
                    #print "distances are ", distances
                    #print min_index
                    distancesL.append(distances)

                    if min_index == firstIndex:
                        values = [distanceI[min_index] for distanceI in distancesL]
                        min_distance_index, min_value = min(enumerate(values), key=operator.itemgetter(1))
                        other_index = (min_index + 1) % 2
                        other_min_distance_index = (min_distance_index + 1 ) % 2 + 1
                        positions_proper[other_min_distance_index] = positions_and_areas[other_index]

                        #pdb.set_trace()
                    firstIndex = min_index

            #print distances
            rawImg = frame.copy()
            for fly_id, fly_features in positions_proper.iteritems():
                x_coordinate = fly_features[0]
                for image in [bigContourFrame, rawImg, bigAndOnlyFlyContourFrame]:
                    cv2.putText(image,
                            str(fly_id),
                            (x_coordinate, 18),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.75,
                            (255,255,255))
            #print "This is the positions_proper", positions_proper
            self.positionsD = positions_proper
            self.collisionLength = 0

            if self.writeRawImages: self.writeRawImagesWithNumbers(self.stitchImages([rawImg]))
        else:
            self.collisionLength += 1


        #print positions
        # Images to show.
        imagesForVideoL = [
               frame,
               self.gray,
               self.diff,
               self.binary,
               allContourFrame,
               bigContourFrame,
               bigAndOnlyFlyContourFrame,
               boundingRectFrame
                ]

        imagesToShowL = imagesForVideoL + maskedL

        stitched = self.stitchImages(imagesToShowL)

        if self.counter > 0: # don't get rid of this
            # adding key handlers and showign the stitched image
            cv2.imshow("stitched", stitched)
            self.addKeyHandlers()

        if self.writeContourVideo: self.writeAllVideo(imagesForVideoL)

        if self.writeData: self.writeDataFile(positions_proper, bigAndFlyContours)

        if self.writeContourImages: self.writeImages(self.stitchImages([bigAndOnlyFlyContourFrame]), self.contourImgDir)

        # writing debugging images
        self.writeImages(self.stitchImages(imagesForVideoL), self.debug_imgs_dir)

        # test_masked = 300
        # if self.counter % test_masked == 0: pdb.set_trace()

        # if len(bigcontours) >= 3:
        #     pdb.set_trace()
        #print '----------------------'
        return positions

    def writeRawImagesWithNumbers(self, image):
        cv2.imwrite(os.path.join(self.rawImgDir, "frame%s.png" % self.counter), image)

    def writeImages(self, image, directory):
        cv2.imwrite(os.path.join(directory, "frame%s.png" % self.counter), image)

    def getPositions(self, bigcontours):
        positions = []
        for i in bigcontours:
            M = cv2.moments(i)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            positions.append([cx, cy])
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
                for i in ["1", "2"]:
                    positions_proper[i] = [configurations.collision_value]*5

            if self.counter == 1:
                string = ">"
            elif self.counter > 1:
                string = ">>"
            else:
                raise ValueError("self.counter is less than 1")

            for i in positions_proper:
                coordinatesL = positions_proper[i][:2]
                area = positions_proper[i][2]
                grayscale_value = positions_proper[i][3]
                width = positions_proper[i][4]

                os.system("echo '%s,fly%s,%s,%s,%s,%s,%s' %s %s" % (
                    self.counter,
                    i,
                    coordinatesL[0],
                    coordinatesL[1],
                    area,
                    grayscale_value,
                    width,
                    string,
                    self.dataFilePathS))

            os.system("echo %s %s %s" % (len(bigcontours), string, self.test_rleFilePathS))

        
    # this function is broken. don't use it
    def writeSingleContourVideos(self):
        if self.counter < 600 and len(bigcontours) ==1:
            if not self.previousIsOne:
                #self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
                imageToWrite = self.stitchImages([bigContourFrame])
                print imageToWrite.shape
                fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
                self.out = cv2.VideoWriter('output%s.mp4' % self.counter ,
                        fourcc, self.fps, (imageToWrite.shape[0],imageToWrite.shape[1]))
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


    def getOnlyFlyContourAndMean(self, bigcontours,contourAreas):
        mean_valuesL  = []
        maskedL = []
        if len(bigcontours) == 0:
            maskedL = [np.zeros(self.gray.shape,np.uint8)]


        for index, bigcontourNP in enumerate(bigcontours):

            masked = np.zeros(self.gray.shape, np.uint8)
            #print len(bigcontours)
            cv2.drawContours(masked, bigcontours, index, (255, 255, 0), -1)

            pixelpoints = np.transpose(np.nonzero(masked))
            mean_val = cv2.mean(self.gray, mask = masked)
            mean_valuesL.append(mean_val)
            maskedL.append(masked)

        #print mean_valuesL

        fly_mean_and_contour = [item for index, item in enumerate(zip(mean_valuesL, bigcontours, contourAreas)) if item[0][0] < self.maxFlyGrayScaleValue]

        return mean_valuesL, maskedL, fly_mean_and_contour

    def getWidthOfContours(self, contourL, contourFrame):

        im = contourFrame.copy()
        widthsL = []

        for cnt in contourL:
            rect = cv2.minAreaRect(cnt)
            width = rect[1][1]
            widthsL.append(width)

            box = cv2.cv.BoxPoints(rect)


            box = np.int0(box)
            cv2.drawContours(im, [box], -1, (0, 0, 255),1)
        return im, widthsL