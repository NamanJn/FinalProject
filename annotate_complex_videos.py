
import configurations
import video_validation
from os.path import join
import pandas as pd
from sklearn.svm import SVC
import pdb

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

    pdb.set_trace()
    trainingFeatures = featuresPD[0:numOfVideosForTraining]
    trainingLabels = labelsPD[0:numOfVideosForTraining]

    testingFeatures = featuresPD[numOfVideosForTraining:]
    testingLabels = labelsPD[numOfVideosForTraining:]


    for i in ["rbf", "linear", "poly"][:3]:
        clf = SVC()
        clf.kernel = i
        print 'training now'
        clf.fit(trainingFeatures.values, trainingLabels.values)

        print 'predicting now'
        print clf.predict(testingFeatures.values)

    # using 4 machine learning algorithms.
    # SVM - linear kernel
    # SVM - polynomial kernel with degree 3
    # SVM -  polynomial kernel with degree 1
    # SVM - rbf kernel
    # logistic regression - linear polynomial
