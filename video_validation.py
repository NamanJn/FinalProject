#!/home/naman/miniconda/bin/python2.7

"""
Usage:
        validate2.py <results_directory> <username>

"""

import inspect 
import cv2
import pdb
import os
#from twoflies import Tracker
from configurations import validation_results_dir
import configurations
import re
import docopt
# This script's aim is to get input from a user
# whether the tracking system switched the identity or no
# Ths userinput will just be "yes" or "no".
# If yes, then switch the identities downstream of the collision.
# If no, then nothing is changed downstream. 



class InspectVideo(object):
    def __init__(self, video_dir_pathS):

        self.video_dir_pathS = video_dir_pathS
        self.video_number = None
    def playVideo(self,video_pathS):

        counter = 0
        cap = cv2.VideoCapture(video_pathS)
        ret, frame = cap.read()
        cv2.imshow("image", frame)
        while True:
            print "press a to continue"
            print "playing video", os.path.basename(video_pathS)
            aKey = cv2.waitKey(0)
            if aKey == ord("a"):
                break


        frame_shape = frame.shape
        write_video = False

        while True:
                breakloop = False

                cv2.waitKey(100)
                ret, frame = cap.read()

                if not ret:
                    while True:
                        #aKey = cv2.waitKey(0)
                        #if aKey == ord("a"):
                            breakloop = True
                            break

                if breakloop:
                    break

                cv2.imshow("image", frame)
                counter += 1

    def inspectVideos(self, video_dirS, output_results_dirS, output_fileS):

        self.video_dirS = video_dirS
        self.videosL = os.listdir(video_dirS)
        videosL = sorted(self.videosL, key= lambda x: int(re.findall(r"collision(\d+)_", x)[0]))
        self.output_file_pathS = os.path.join(output_results_dirS, validation_results_dir, output_fileS)

        pdb.set_trace()
        self.video_number = 0

        #for videoS in videosL[::-1]:
        while self.video_number < len(videosL):
            # reading the video
            #collisionFrame = 916
            #cap = cv2.VideoCapture("collision_vids/collision%s_withcontours.mp4" % collisionFrame)
            videoS = videosL[self.video_number]

            self.collisionFrame = int(re.findall(r"collision(\d+)_", videoS)[0])
            print "playing collision video:", videoS
            self.playVideo(os.path.join(video_dirS, videoS))

            self.askUserForAnswer()
            # showing the first image and waiting for 2 clicks

        print "finished!"

    def askUserForAnswer(self):
            while True:
                x = raw_input("Did identities switch? [y/n/r/p]: ")
                if x == "y" or x == "n":

                    if x == "y":
                        print "ok switched"

                    elif x == "n":
                        print "ok didn't switch"

                    self.video_number += 1
                    os.system("echo '%s,%s,%s' >> %s" % (self.collisionFrame, x, currentUser, self.output_file_pathS))
                    break
                elif x == "r":
                    print "playing again chosen.... press a to continue"
                    self.playVideo(os.path.join(self.video_dirS, videoS))
                elif x == "p":
                    print "playing previous video again chosen.... press a to continue"
                    self.video_number -= 1
                    videoS = self.videosL[::-1][self.video_number]
                    self.playVideo(os.path.join(self.video_dirS, videoS))
                else:
                    print "try again"



if __name__ == "__main__":
    d = docopt.docopt(__doc__)
    currentUser = d['<username>']
    results_dir_pathS = os.path.join(configurations.output_dir, d['<results_directory>'] )
    ee = execfile
    inspectVideo = InspectVideo("collision_vids/")
    inspectVideo.inspectVideos("collision_vids", results_dir_pathS, 'identity.csv')
