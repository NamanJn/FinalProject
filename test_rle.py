import inspect
import os
ee = execfile
poing = inspect.getabsfile(inspect.currentframe())
import pdb
import configurations
from collections import Counter
from os.path import join
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
def myencode(string):
    
    prev = string[0]
    current_length = []
    count = 1
    output = []
    counter = 1
    for char in string[1:]:
        if char == prev:
            count +=1
        else:
            outputSize = len(output)
            output.append([prev,count, counter - count+1, outputSize])
            count = 1
        prev = char
        counter += 1
    outputSize = len(output)
    output.append([prev,count,counter - count+1, outputSize])
    return output

def readcsv(string):
    openfile = open(string)
    readfile = openfile.read()
    openfile.close()
    return readfile.replace("\n","")



def cutvideo(startFrame,length):
    # This is to cut the video from start-end time.
    frame_rate = 25.0
    buffer_time_before_collision = 0.5 
    buffer_time_after = 0.1 
    collision_start_time = startFrame/frame_rate
    collision_duration_time = length/frame_rate

    start_time = collision_start_time - buffer_time_before_collision #+ 500/frame_rate
    
    print "start_time is ", start_time
    end_time = collision_start_time + collision_duration_time  + buffer_time_after
    print "the end_time is ", end_time
    #pdb.set_trace()

    os.system("ffmpeg -i 2flies.mp4 -vf trim=%s:%s ennot.mp4 -y" 
            %(start_time, end_time))

    # this is to crop the video to get just the ROI
    os.system('ffmpeg -i ennot.mp4 -filter:v "crop=500:23:70:261" cropped.mp4 -y')

    # This is to rescale the video
    os.system("ffmpeg -i cropped.mp4 -vf scale=1000:46 collision%s.mp4 -y" % startFrame)


def cutContourVideo(startFrame, length, directory):

    # This is to cut the video from start-end time.
    frame_rate = float(configurations.fps)
    buffer_time_before_collision = 2
    buffer_time_after = 0.1
    collision_start_time = startFrame/frame_rate
    collision_duration_time = length/frame_rate

    start_time = collision_start_time - buffer_time_before_collision #+ 500/frame_rate

    print "start_time is ", start_time
    end_time = collision_start_time + collision_duration_time + buffer_time_after
    print "the end_time is ", end_time
    pdb.set_trace()
    #pdb.set_trace()

    stringToExecute = "ffmpeg -i output_multipleframes.avi -vf trim=%s:%s %s/collision%s_withcontours.mp4 -y" % (start_time,
                                                                                                  end_time,
                                                                                                  directory,
                                                                                                  startFrame)

    #pdb.set_trace()
    os.system(stringToExecute)

def readAndCreateRle(string):

    rawString = readcsv(string)
    rawString = rawString.replace("0", "1")
    rawString = rawString.replace("3", "2")
    rle = myencode(rawString) # replacing 0s with 1s.


    return rle

def getInterCollisionsFromDataFile(user_dir):

    # right now this function only gets in the area
    results_dir_path = join(configurations.output_dir, user_dir) # user_dir the folder beneath the 'output' dir.
    data_file_path = join(results_dir_path, configurations.data_file)
    interCollisionsAreaL = []
    dF = pd.read_csv(data_file_path, names=configurations.col_names)

    num_of_rows = dF.shape[0]

    tempo = []
    counter = 0
    values = dF.values

    # finding the width to check whether it occurs during a collision or no.
    widthIndex = configurations.col_names.index('width')
    areaIndex = configurations.col_names.index('area')

    for rowIndexI in range(num_of_rows):
        #theRow = dF.iloc[rowIndexI, :]
        theRow = values[rowIndexI, :]

        # theWidth = theRow.width
        # theArea = theRow.area
        theWidth = theRow[widthIndex]
        theArea = theRow[areaIndex]

        if theWidth == configurations.collision_value:
            if tempo != []:
                interCollisionsAreaL.append(np.array(tempo))
            tempo = []
        else:
            tempo.append(theRow)

        counter += 1
        print counter
        #if counter > 170: pdb.set_trace()


    return interCollisionsAreaL

def getCollisionAreas(user_dir):
    results_dir_path = join(configurations.output_dir, user_dir) # user_dir the folder beneath the 'output' dir.
    data_file_path = join(results_dir_path, configurations.data_file)
    interCollisionsAreaL = []
    dF = pd.read_csv(data_file_path, names=configurations.col_names)

    num_of_rows = dF.shape[0]

    tempo = []
    counter = 0
    values = dF.values

    # finding the width to check whether it occurs during a collision or no.
    widthIndex = configurations.col_names.index('width')
    areaIndex = configurations.col_names.index('area')

    for rowIndexI in range(num_of_rows):
        #theRow = dF.iloc[rowIndexI, :]
        theRow = values[rowIndexI, :]

        # theWidth = theRow.width
        # theArea = theRow.area
        theWidth = theRow[widthIndex]
        theArea = theRow[areaIndex]

        if theWidth != configurations.collision_value:
            if tempo != []:
                interCollisionsAreaL.append(tempo)
            tempo = []
        else:
            tempo.append(theArea)

        counter += 1
        print counter
        #if counter > 170: pdb.set_trace()

    return interCollisionsAreaL


def createComplexVideos(rle, twos, complex_collisionsL, user_dir, buffer_time):

    results_dir_path = join(configurations.output_dir, user_dir) # user_dir the folder beneath the 'output' dir.
    source_directory = join(results_dir_path, configurations.debug_images_dir)
    annotations_file_path = join(results_dir_path, 'annotations.csv')
    data_file_path = join(results_dir_path, configurations.data_file)

    collisionLengthsL = []

    collisionAreasL = getCollisionAreas('tube4_3thSep')

    counter = 0
    for i in complex_collisionsL:

        indexOfFirstInterCollision = i[2]-1
        indexOfLastInterCollision = i[2]-1 + i[1]-1

        firstInterCollision = twos[indexOfFirstInterCollision]
        lastInterCollision = twos[indexOfLastInterCollision]

        num_of_collisions = i[1]+1

        lengthOfInterCollisions = [item[1] for item in twos[indexOfFirstInterCollision:indexOfLastInterCollision+1]]
        averageLengthOfInterCollisions = sum(lengthOfInterCollisions)/float(len(lengthOfInterCollisions))


        indexOfStartingCollision = firstInterCollision[3]-1
        startingCollision = rle[firstInterCollision[3]-1]

        if lastInterCollision[3] + 1 == len(rle):
            indexOfLastCollision =  lastInterCollision[3]-1

        else:
            indexOfLastCollision = lastInterCollision[3]+1

        endingCollision = rle[indexOfLastCollision]


        # finding the average collision contour size
        pdb.set_trace()
        collisionContourSizesL = [collisionAreasL[j[3]] for j in rle[indexOfStartingCollision: indexOfLastCollision+1] if j[0] == "1"]
        flattenedCollisionContourSizesL = [k for j in collisionContourSizesL for k in j]
        totalCollisionContourSize = sum(flattenedCollisionContourSizesL)
        averageCollisionContourSize = totalCollisionContourSize/float(len(flattenedCollisionContourSizesL))

        collisionLength = endingCollision[2]+endingCollision[1] - startingCollision[2] + 1
        collisionStartFrame = startingCollision[2]

        collisionLengthsL.append(collisionLength)
        collision_len_time = collisionLength/float(configurations.fps)


        #createVideoFromImages(collisionStartFrame, collisionLength, source_directory, configurations.complex_video_dir, bufferTime=buffer_time)
        if counter == 0:
            pipe_string = ">"
        else:
            pipe_string = ">>"
        os.system("echo '%s,%s,%s,%s,%s' %s %s" % (collisionStartFrame, num_of_collisions, collision_len_time, averageLengthOfInterCollisions,
                                                averageCollisionContourSize, pipe_string, annotations_file_path))

        counter += 1

def createSimpleCollisionVideos(rle):

    simple_collisionsL = []
    interCollisionFrameThreshold = configurations.interCollisionTime * configurations.fps
    #for every collision, I want to see on either side if they are longer than 6 seconds.
    for index, item in enumerate(rle):

        if item[0] == "1":

            # checking length of previous intercollision
            before_length = rle[index-1][1]
            # checking length of after intercollision
            after_length = rle[index+1][1]
            if before_length >= interCollisionFrameThreshold and after_length >= interCollisionFrameThreshold:
                simple_collisionsL.append(item)
                createVideoFromImages(item[2], item[1], configurations.debug_images_dir, configurations.simple_collision_dir)


def createCollisionVideos(source_dir_pathS, sink_dir_pathS, threshold_for_short):

    fileNameS = configurations.rle_data_file
    rle = readAndCreateRle(fileNameS)

    ones = [i for i in rle if i[0] == "1"]
    print ones

    #cutvideo(663, 8)
    # creating chunks of the videos.
    for i, collisionLength, collisionStartFrame, index in ones:
        if collisionStartFrame > 300:
            video_suffix = ""
            if collisionLength <= threshold_for_short:
                video_suffix = "_short"
            createVideoFromImages(collisionStartFrame, collisionLength, source_dir_pathS, sink_dir_pathS, video_suffix=video_suffix)
            #cutContourVideo(collisionStartFrame, collisionLength)

def createVideoFromImages(startFrame, collisionLength, source_directory, sinkDirectory, bufferTime=1 , video_suffix=""):

    imageDirectory = source_directory

    fps = configurations.fps
    buffer_time_frames = int(bufferTime*fps)
    videoStartFrame = startFrame - buffer_time_frames

    collisionLengthWithBuffer = collisionLength + 2*buffer_time_frames
    stringToExecute = 'ffmpeg -start_number %s -framerate %s -i %s/frame%%d.png -vframes %s -vcodec mpeg4 %s/collision%s%s.mp4 -y' % (videoStartFrame,
                                                                                                                       fps,
                                                                                                                       imageDirectory,
                                                                                                                       collisionLengthWithBuffer,
    sinkDirectory, startFrame,video_suffix)

    os.system(stringToExecute)

def createHistogramOfCollisionLengths(user_dir):

    # This creates a histogram of the collision lengths

    results_dir = os.path.join(configurations.output_dir, user_dir)
    rle = readAndCreateRle(join(results_dir, configurations.rle_data_file))
    ones = [ i for i in rle if i[0] == "1" ]

    collisionLengthsL = [i[1] for i in ones]
    moreThan23L = []
    thresholdForGrouping = 24
    for i in collisionLengthsL:
        if i >= thresholdForGrouping: moreThan23L.append(thresholdForGrouping)
        else: moreThan23L.append(i)

    heightsForBarChart = dict(Counter(moreThan23L)).values()

    fps = configurations.fps
    lastValue = str((thresholdForGrouping - 1)/float(fps))
    xAxisLabelsL = [str(i/float(fps)) for i in range(1, thresholdForGrouping)]+[">  %s" % lastValue]

    # plotting the graph
    createHistogram("collisionLengthDistribution.png", heightsForBarChart, "Collision length (seconds)",
                    "Frequency", xAxisLabelsL=xAxisLabelsL)

def createHistogram(histogramNameS, dataL, xAxisTitleS, yAxisTitleS, xAxisLabelsL ):

    df = pd.DataFrame(dataL)
    ax = df.plot(kind="bar")

    ax.set_xticklabels(xAxisLabelsL)
    ax.legend_.remove()
    sns.plt.xlabel(xAxisTitleS)
    sns.plt.ylabel(yAxisTitleS)
    sns.plt.tight_layout()
    sns.plt.savefig(histogramNameS)


if __name__ == "__main__":

    user_dir = "tube4"
    results_dir = os.path.join(configurations.output_dir, user_dir)
    rle = readAndCreateRle(join(results_dir, configurations.rle_data_file))

    ones = [ i for i in rle if i[0] == "1" ]
    twos = [ i for i in rle if i[0] == "2" ]

    interCollisionTimeThreshold = configurations.interCollisionTime # This is in seconds.
    interCollisionFrameThreshold = interCollisionTimeThreshold*configurations.fps
    intercollisionLength = map(lambda x: x[1] < interCollisionFrameThreshold, twos)
    rle_intercollision = myencode(intercollisionLength)

    # getting the positions of intercollision frames that are less than 20 frames
    complex_collisionsL = []

    for i in rle_intercollision:
        if i[0] == True and i[1] > 1:
            complex_collisionsL.append(i)


    source_dir_pathS = os.path.join(results_dir, configurations.debug_images_dir)
    sink_dir_pathS = configurations.collision_dir
    #createCollisionVideos(source_dir_pathS=source_dir_pathS, sink_dir_pathS=sink_dir_pathS, threshold_for_short=3)

    # This is to create the videos.
    collisionLengthsL = createComplexVideos(rle, twos, complex_collisionsL[:103], user_dir, buffer_time=2)
    #interCollisionsAreaL = getInterCollisionsFromDataFile(user_dir)
    #collisionsAreaL = getCollisionAreas(user_dir+"_3thSep")



