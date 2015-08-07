
from sklearn.cluster import KMeans
import inspect
import numpy as np
poing = inspect.getabsfile(inspect.currentframe())
ee = execfile
import pandas as pd
from configurations import col_names

feature_set = np.array([[7.65235, 2.08],
                [6.3, 1.4],
                [0.93, 3.73],
                [-1.5, -3.75]])



generated = pd.read_csv("data_shortcoll.csv", names=col_names)


km = KMeans(n_clusters=2)
labels = km.fit(feature_set).labels_





