import inspect
import os
ee = execfile
poing = inspect.getabsfile(inspect.currentframe())
import pdb
import configurations
from collections import Counter
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


def createComplexVideos(rle, twos, complex_collisionsL):
    collisionLengthsL = []
    for i in complex_collisionsL:
        firstInterCollision = twos[i[2]-1]
        lastInterCollision = twos[i[2]-1 + i[1]-1]
        startingCollision = rle[firstInterCollision[3]-1]
        if lastInterCollision[3] + 1 == len(rle):
            endingCollision = rle[lastInterCollision[3]-1]
        else:
            endingCollision = rle[lastInterCollision[3]+1]

        collisionLength = endingCollision[2]+endingCollision[1] - startingCollision[2] + 1
        collisionStartFrame = startingCollision[2]

        collisionLengthsL.append(collisionLength)
        #pdb.set_trace()
        createVideoFromImages(collisionStartFrame, collisionLength, configurations.debug_images_dir, configurations.complex_video_dir)



def createCollisionVideos():

    fileNameS = configurations.rle_data_file
    rle = readAndCreateRle(fileNameS)

    ones = [ i for i in rle if i[0] == "1" ]
    print ones

    #cutvideo(663, 8)
    # creating chunks of the videos.
    for i, collisionLength, collisionStartFrame, index in ones:
        if collisionStartFrame > 300:
            cutContourVideo(collisionStartFrame, collisionLength)

def createVideoFromImages(startFrame, collisionLength, directory, sinkDirectory, bufferTime = 10 ):

    imageDirectory = directory

    fps = configurations.fps

    videoStartFrame = startFrame - bufferTime

    collisionLengthWithBuffer = collisionLength + 2*bufferTime
    stringToExecute = 'ffmpeg -start_number %s -framerate %s -i %s/frame%%d.png -vframes %s -vcodec mpeg4 %s/collision%s.mp4 -y' % (videoStartFrame,
                                                                                                                       fps,
                                                                                                                       imageDirectory,
                                                                                                                       collisionLengthWithBuffer,
    sinkDirectory, startFrame)

    os.system(stringToExecute)

if __name__ == "__main__":


    rle = readAndCreateRle(configurations.rle_data_file)

    ones = [ i for i in rle if i[0] == "1" ]
    twos = [ i for i in rle if i[0] == "2" ]

    interCollisionTimeThreshold = 6 # This is in seconds.
    interCollisionFrameThreshold = interCollisionTimeThreshold*configurations.fps
    intercollisionLength = map(lambda x: x[1] < interCollisionFrameThreshold, twos)
    rle_intercollision = myencode(intercollisionLength)

    # getting the positions of intercollision frames that are less than 20 frames
    complex_collisionsL = []

    for i in rle_intercollision:
        if i[0] == True and i[1] > 1:
            complex_collisionsL.append(i)

    simple_collisionsL = []
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

    #collisionLengthsL = createComplexVideos(rle,twos,complex_collisionsL)
    #collisionLengthsDistribution = Counter(collisionLengthsL)
    #print collisionLengthsDistribution

