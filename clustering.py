
"""
Usage:
        clustering.py <results_directory>

"""

from sklearn.cluster import KMeans
import inspect
import numpy as np
import pandas as pd
import os
from configurations import col_names, data_dir, collision_value, data_file
import docopt
import sys

poing = inspect.getabsfile(inspect.currentframe())
ee = execfile

d = docopt.docopt(__doc__)
results_directory = d['<results_directory>']
print "This is the resultsdirectory", results_directory
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


feature_set = nonCollisions.iloc[:, 4:]

km = KMeans(n_clusters=2)
labels = km.fit(feature_set).labels_


