
from configurations import data_dir,corrected_data_dir
import os
import pandas as pd
import inspect
from test_rle import readAndCreateRle

ee = execfile
poing = inspect.getabsfile(inspect.currentframe())


dataFileS = "data_shortcoll.csv"
dataFilePathS = os.path.join(data_dir, dataFileS)

rleFileS = "csv.csv"
rleFilePathS = os.path.join(data_dir, rleFileS)


rle = readAndCreateRle(rleFilePathS)
raw_data = pd.read_csv(dataFilePathS)


