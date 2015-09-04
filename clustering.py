
"""
Usage:
        clustering.py <results_directory>

"""
import test_rle
import pdb
from sklearn.cluster import KMeans
import inspect
import numpy as np
import pandas as pd
import os
from configurations import col_names, data_dir, collision_value, data_file
import docopt
import sys
import configurations
poing = inspect.getabsfile(inspect.currentframe())
ee = execfile

# d = docopt.docopt(__doc__)
# results_directory = os.path.join(configurations.output_dir, d['<results_directory>'])
results_directory = os.path.join(configurations.output_dir, 'tube4')
print "This is the results directory", results_directory
dataFilePathS = os.path.join(results_directory, data_file)

if not os.path.exists(dataFilePathS):
   print "Directory doesn't exist! you need to run the analysis!"
   sys.exit()


feature_set = np.array([[7.65235, 2.08],
                [6.3, 1.4],
                [0.93, 3.73],
                [-1.5, -3.75]])


generated = pd.read_csv(dataFilePathS, names=col_names)


# getting non-collisions by filtering via the 'fly width' column
nonCollisions = generated[generated.width != collision_value]
nonCollisionsL = test_rle.getInterCollisionsFromDataFile('tube4')

# this gets the average values of features per fly per set of intercollision frames
featuresPerFlyPerInterCollision = []
for i in nonCollisionsL:
    fly1 = i[i[:, 1] == "fly1"]
    fly2 = i[i[:, 1] == "fly2"]
    fly1Average = np.average(fly1[:, 4:], axis=0).astype("float64")
    fly2Average = np.average(fly2[:, 4:], axis=0).astype("float64")

    isnan1 = np.isnan(fly1Average)
    isnan2 = np.isnan(fly2Average)
    if isnan1.any() or isnan2.any(): pdb.set_trace()
    featuresPerFlyPerInterCollision.append([fly1Average, fly2Average])


# clustering on features per fly per frame
feature_set = nonCollisions.iloc[:, 4:]

km = KMeans(n_clusters=2)
labels = km.fit(feature_set).labels_

# clustering on features per fly per set of IC frames
flattenedFeaturesPerFlyPerInterCollision = np.array([j for i in featuresPerFlyPerInterCollision for j in i])

km = KMeans(n_clusters=2)
labels = km.fit(flattenedFeaturesPerFlyPerInterCollision).labels_

