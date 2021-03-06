
"""
Usage:
        position_validate.py <results_directory>

"""

import inspect
import cv2
import os
import configurations
import numpy as np
import docopt


class ImgListener(object):

    def __init__(self, frame):

        self.imageFrame = frame
        self.positionsL = []
        self.real_positionsL = []

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.listen_for_click, param=2)

    def listen_for_click(self, event, x, y, flags, param):
        """
        This method is the event listener for the position clicked by user.
        :param event: Type of event.
        :param x: x-coordinate clicked by user.
        :param y: y-coordinate clicked by user.
        :param flags: -
        :param param: -
        :return: None
        """

        if event == cv2.EVENT_LBUTTONUP and len(self.positionsL) < param:
            print x, y
            self.positionsL.append([x,y])

            coordinates = list(np.array([x, y])/2)
            self.real_positionsL.append(coordinates)


    def show(self):
        """
        This method displays the current frame to the user.
        :return: None
        """
        cv2.imshow("image", self.imageFrame)


if __name__ == "__main__":

    ee = execfile
    d = docopt.docopt(__doc__)
    results_directory = os.path.join(configurations.output_dir, d['<results_directory>'])

    if not os.path.exists(results_directory):
        raise EnvironmentError("The '%s' does not exist. It probably means you have not run the analysis yet" % results_directory )


    dir_path = os.path.join(results_directory, configurations.raw_imgs_dir)
    results_file = "position_validation.csv"


    validation_results_dir = os.path.join(results_directory, configurations.validation_results_dir)
    fileToWriteResults = os.path.join(validation_results_dir, results_file)

    # create directory if doesn't exist.
    if not os.path.isdir(validation_results_dir):
        os.makedirs(validation_results_dir)

    counter = 0
    frame_interval = 150
    for i in range(300, 40000, frame_interval):

        counter += 1
        img_nameS = "frame%s.png" % i
        print "image is %s" % img_nameS
        image_path = os.path.join(dir_path, img_nameS)

        if os.path.exists(image_path):
            print 'Image path is', image_path
            print 'Reading image now'
            frame = cv2.imread(image_path)
        else:
            print img_nameS, 'does not exist'
            continue

        listener = ImgListener(frame)

        # showing the first image and waiting for 2 clicks
        print 'Showing image now'
        listener.show()


        print "Press 's' to skip to next image"
        print "Press 'a' once you are done clicking both flies"
        print "You need to click the number 1 fly first."
        while True:

            aKey = cv2.waitKey(0) 

            if aKey == ord("a") and len(listener.positionsL) == 2:
                for index, positionsL in enumerate(listener.real_positionsL):
                    os.system("echo '%s,fly%s,%s,%s' >> %s" % (i, 
                        index+1,
                        positionsL[0],
                        positionsL[1],
                        fileToWriteResults))
                break
            elif aKey == ord("s"):
                break

