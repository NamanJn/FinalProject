import inspect
import os
ee = execfile
poing = inspect.getabsfile(inspect.currentframe())
import pdb
import configurations

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
            output.append([prev,count, counter - count+1])
            count = 1
        prev = char
        counter += 1
    output.append([prev,count,counter - count+1])
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


def cutContourVideo(startFrame,length):
    # This is to cut the video from start-end time.
    frame_rate = configurations.fps
    buffer_time_before_collision = 0.1
    buffer_time_after = 0.05
    collision_start_time = startFrame/frame_rate
    collision_duration_time = length/frame_rate

    start_time = collision_start_time - buffer_time_before_collision #+ 500/frame_rate
    
    print "start_time is ", start_time
    end_time = collision_start_time + collision_duration_time  + buffer_time_after
    print "the end_time is ", end_time
    #pdb.set_trace()

    stringToExecute = "ffmpeg -i output1.avi -vf trim=%s:%s collision_vids/collision%s_withcontours.mp4 -y" %(start_time, end_time,startFrame)

    #pdb.set_trace()
    os.system(stringToExecute)

def readAndCreateRle(string):

    rawString = readcsv(string)
    rawString = rawString.replace("0", "1")
    rawString = rawString.replace("3", "2")
    rle = myencode(rawString) # replacing 0s with 1s.


    return rle


def createComplexVideos():
    pass


def createCollisionVideos():

    fileNameS = configurations.rle_data_file

    rle = readAndCreateRle(fileNameS)

    ones = [ i for i in rle if i[0] == "1" ]
    print ones

    #cutvideo(663, 8)
    # creating chunks of the videos.
    for i, collisionLength, collisionStartFrame in ones:
        if collisionStartFrame > 300:
            cutContourVideo(collisionStartFrame, collisionLength)


if __name__ == "__main__":


    rle = readAndCreateRle(configurations.rle_data_file)

    ones = [ i for i in rle if i[0] == "1" ]
    twos = [ i for i in rle if i[0] == "2" ]

    intercollisionLength = map(lambda x: x[1] < 20, twos)
    rle_intercollision = myencode(intercollisionLength)

    # getting the positions of intercollision frames that are less than 20 frames
    complex_collisionsL = [i for i in rle_intercollision if i[0] == True and i[1] > 1 ]

    # getting collisionStartFrame and collisionLength to start cutting the complex videos
    for i in complex_collisionsL:
        firstInterCollision = twos[i[2]-1]
        lastInterCollision = twos[i[2]-1 + i[1]-1]
        startingCollision = None
        endingCollision = None
