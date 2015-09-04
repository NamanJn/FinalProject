
import configurations
import video_validation
from os.path import join
import pandas as pd
from sklearn.svm import SVC
import pdb
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import test_rle
import numpy as np

def annotateVideos():

    complex_vids_dirS = 'complex_collision_vids'

    complex_annotation = video_validation.InspectVideos(complex_vids_dirS, 'what type is it?',
                                                        ["1", "2", "3"], regex=r"collision(\d+)")

    complex_annotation.output_file_pathS = 'output/tube4/validation_results/type_annotated.csv'
    complex_annotation.inspectVideos(complex_vids_dirS, 'tube4', 'type_annotated.csv', repeat_validation=False)
    #complex_annotation.getRemainingVideosToValidate()

def trainAnnotatedVideos(user_dir):

    results_dir_path = join(configurations.output_dir, user_dir)
    features_file_path = join(results_dir_path, configurations.features_file)

    # using 100 videos to train support vector machine and 50 videos for testing
    featuresFilePD = pd.read_csv(features_file_path, header=None)
    featuresPD = featuresFilePD.iloc[:, 1:]

    labelsFilePD = pd.read_csv(configurations.annotations_file, header=None)
    labelsPD = labelsFilePD.iloc[:, 1]

    numOfVideosForTraining = 100

    # training set
    trainingFeatures = featuresPD[0:numOfVideosForTraining]
    trainingLabels = labelsPD[0:numOfVideosForTraining]

    # testing set
    testingFeatures = featuresPD[numOfVideosForTraining:]
    testingLabels = labelsPD[numOfVideosForTraining:]


    # using 4 machine learning algorithms.
    # SVM - linear kernel
    # SVM - polynomial kernel with degree 3
    # SVM -  polynomial kernel with degree 1
    # SVM - rbf kernel
    # logistic regression - linear polynomial

    accuraciesD = {}
    for i in ["SVM-rbf", "SVM-linear", "SVM-sigmoid", "SVM-poly", "logistic", "k-NN"]:

        if i == "logistic":
            clf = LogisticRegression()

        elif i == "k-NN":
            clf = KNeighborsClassifier()

        elif i[:3] == "SVM":
            clf = SVC()
            kernelType = i.split("-")[-1]
            clf.kernel = kernelType
            if kernelType == "poly":
                clf.degree = 1

        print 'training now'
        clf.fit(trainingFeatures.values, trainingLabels.values)

        print 'predicting now'
        predictedNP = clf.predict(testingFeatures.values)

        print clf.score(testingFeatures.values, testingLabels.values)

        # testing accuracy
        BooleanNP = predictedNP == testingLabels.values
        frequenciesD = Counter(BooleanNP)
        accuracyI = frequenciesD[True]/float(sum(frequenciesD.values()))
        accuraciesD[i] = accuracyI
        print "the accuracy of %s is %s\n" % (i, accuraciesD[i])

    print accuraciesD
    return accuraciesD

def createHistogramForClassifierResults():
    accuraciesD = trainAnnotatedVideos('tube4')
    dataL = np.array(accuraciesD.values())*100
    xAxisLabelsL = accuraciesD.keys()
    test_rle.createHistogram("classifier.png", dataL, xAxisTitleS='Algorithms', yAxisTitleS='Accuracy (%)',
                             xAxisLabelsL=xAxisLabelsL, clockWiseAngleOfXLabels=90)

if __name__ == "__main__":

    user_dir = 'tube4'
    accuraciesD = trainAnnotatedVideos(user_dir)
    createHistogramForClassifierResults()
