
from sklearn.cluster import KMeans
import inspect
import numpy as np
poing = inspect.getabsfile(inspect.currentframe())
ee = execfile
import pandas as pd
import os
from configurations import col_names, data_dir, collision_value

feature_set = np.array([[7.65235, 2.08],
                [6.3, 1.4],
                [0.93, 3.73],
                [-1.5, -3.75]])


dataFilePathS = os.path.join(data_dir, "data_shortcoll.csv")
generated = pd.read_csv(dataFilePathS, names=col_names)

# getting non-collisions by filtering via the 'fly width' column
nonCollisions = generated[generated.width != collision_value]


feature_set = nonCollisions.iloc[:, 4:]

km = KMeans(n_clusters=2)
labels = km.fit(feature_set).labels_


