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
import pandas as pd
# This script's aim is to get input from a user
# whether the tracking system switched the identity or no
# Ths userinput will just be "yes" or "no".
# If yes, then switch the identities downstream of the collision.
# If no, then nothing is changed downstream. 



class InspectVideos(object):
    def __init__(self, video_dir_pathS, question, possible_answers, current_validator='someone', regex=r"collision(\d+)_"):

        self.video_dir_pathS = video_dir_pathS
        self.video_number = None
        self.question = question
        self.possible_answers = possible_answers
        self.current_validator = current_validator
        self.regex = regex

    def playVideo(self, video_pathS):

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

    def askUserForAnswer(self):

        while True:
            string_to_ask = "%s [%s/r/p/skip]: " % (self.question, "/".join(self.possible_answers))
            x = raw_input(string_to_ask)

            if x in self.possible_answers:

                print "ok you gave the answer of ", x
                self.video_number += 1
                os.system("echo '%s,%s,%s' >> %s" % (self.collisionFrame, x, self.current_validator, self.output_file_pathS))
                break

            elif x == "r":
                print "playing again chosen.... press a to continue"
                current_video_pathS = os.path.join(self.video_dirS, self.current_videoS)
                self.playVideo(current_video_pathS)

            elif x == "p":
                print "playing previous video again chosen.... press a to continue"
                self.video_number -= 1
                self.current_videoS= self.videosL[::-1][self.video_number]
                self.playVideo(os.path.join(self.video_dirS, self.current_videoS))
            elif x == "skip":
                self.video_number += 1
                print "skipping input"
                break

            else:
                print "try again"

    def inspectVideos(self, video_dirS, output_results_dirS, output_fileS, repeat_validation = True):

        self.video_dirS = video_dirS
        self.videosL = os.listdir(video_dirS)

        if not repeat_validation:
            self.videosL = self.getRemainingVideosToValidate()

        videosL = sorted(self.videosL, key= lambda x: int(re.findall(self.regex, x)[0]))

        self.output_file_pathS = os.path.join(configurations.output_dir, output_results_dirS, validation_results_dir, output_fileS)

        print 'file to save answers is', self.output_file_pathS
        pdb.set_trace()
        self.video_number = 0

        #for videoS in videosL[::-1]:
        while self.video_number < len(videosL):
            # reading the video
            #collisionFrame = 916
            #cap = cv2.VideoCapture("collision_vids/collision%s_withcontours.mp4" % collisionFrame)
            self.current_videoS = videosL[self.video_number]

            self.collisionFrame = int(re.findall(self.regex, self.current_videoS)[0])
            print "playing collision video:", self.current_videoS
            self.playVideo(os.path.join(video_dirS, self.current_videoS))

            # showing the first image and waiting for 2 clicks
            self.askUserForAnswer()

        print "finished!"

    def getRemainingVideosToValidate(self):
        max_video_annotated = 0
        try:
            annotated_file_pd = pd.read_csv(self.output_file_pathS, header=None)
            max_video_annotated = max(annotated_file_pd.values[:, 0])
        except:
            pass
        remaining_videosL = []
        pdb.set_trace()
        for videoS in self.videosL:
            video_collision_frame = int(re.findall(self.regex, videoS)[0])
            if video_collision_frame > max_video_annotated:
                remaining_videosL.append(videoS)


        return remaining_videosL


class InspectComplexVideos(InspectVideos):
    pass

if __name__ == "__main__":
    d = docopt.docopt(__doc__)
    currentUser = d['<username>']
    results_dir_pathS = os.path.join(configurations.output_dir, d['<results_directory>'] )
    ee = execfile
    inspectVideo = InspectVideos("collision_vids/","did it switch?", ["y","n"])
    inspectVideo.inspectVideos("collision_vids", results_dir_pathS, 'identity.csv')
