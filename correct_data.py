
from configurations import data_dir,corrected_data_dir,validation_results_dir,col_names
import os
import pandas as pd
import inspect
from test_rle import readAndCreateRle
import pdb
ee = execfile
poing = inspect.getabsfile(inspect.currentframe())


def flipFrameIdentities(dataFrame):
    dataFrameCopy = dataFrame.copy()
    dataFrameCopy.iloc[0,2:] = dataFrame.iloc[1,2:]
    dataFrameCopy.iloc[1,2:] = dataFrame.iloc[0,2:]
    return dataFrameCopy

dataFileS = "data_shortcoll.csv"
dataFilePathS = os.path.join(data_dir, dataFileS)

rleFileS = "csv.csv"
rleFilePathS = os.path.join(data_dir, rleFileS)

validatedFileS = "identity.csv"
validatedFilePathS = os.path.join(validation_results_dir, validatedFileS)

# reading the files
rle = readAndCreateRle(rleFilePathS)
raw_data = pd.read_csv(dataFilePathS, header=None)
results = pd.read_csv(validatedFilePathS, header=None)

getYes = results[results.icol(1) == "y"]
raw_data_copy = raw_data.copy()

yesValuesL = getYes.values[:, 0]

for i in range(0, len(yesValuesL), 2):

    startingBound = yesValuesL[i]
    upperBound = yesValuesL[i+1]
    print startingBound
    print upperBound

    for j in range(startingBound, upperBound):

        matchingRow = raw_data_copy [raw_data_copy.icol(0) == j]
        indexes = matchingRow.index
        flipped = flipFrameIdentities(matchingRow)
        raw_data_copy.iloc[indexes[0]:indexes[1]+1] = flipped
        print indexes


# raw_data_copy is the final answer

