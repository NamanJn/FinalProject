
import configurations
import video_validation
from os.path import join
import pandas as pd
from sklearn.svm import SVC
import pdb
from collections import Counter

def annotateVideos():

    complex_vids_dirS = 'complex_collision_vids'

    complex_annotation = video_validation.InspectVideos(complex_vids_dirS, 'what type is it?',
                                                        ["1", "2", "3"], regex=r"collision(\d+)")

    complex_annotation.output_file_pathS = 'output/tube4/validation_results/type_annotated.csv'
    complex_annotation.inspectVideos(complex_vids_dirS, 'tube4', 'type_annotated.csv', repeat_validation=False)
    #complex_annotation.getRemainingVideosToValidate()

def trainAnnotatedVideos(user_dir):
    pass


if __name__ == "__main__":

    user_dir = 'tube4'
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
    for i in ["rbf", "linear", "sigmoid", "poly"]:
        clf = SVC()
        clf.kernel = i
        if i == "poly":
            clf.degree = 1

        print 'training now'
        clf.fit(trainingFeatures.values, trainingLabels.values)

        print 'predicting now'
        predictedNP = clf.predict(testingFeatures.values)

        # testing accuracy
        BooleanNP = predictedNP == testingLabels.values
        frequenciesD = Counter(BooleanNP)
        accuracyI = frequenciesD[True]/float(sum(frequenciesD.values()))
        accuraciesD[i] = accuracyI
        print "the accuracy of %s is %s\n" % (i, accuraciesD[i])

    print accuraciesD

