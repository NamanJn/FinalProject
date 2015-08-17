
from configurations import data_dir, corrected_data_dir, validation_results_dir, col_names
import os
import pandas as pd
import inspect
from test_rle import readAndCreateRle
import pdb
ee = execfile
poing = inspect.getabsfile(inspect.currentframe())


class CorrectCollisions(object):
    def __init__(self, data_file, validated_results, rle):
        self.data_file = data_file
        self.validated_results = validated_results
        self.rle = rle
        self.correctedData = None
        self.yes_valuesL = self.validated_results[self.validated_results.icol(1) == "y"].values[:,0]

    def getCorrectedData(self):
        if self.correctedData == None:
            self.correctedData = 5   # fix this.
        return self.correctedData

    def get_switched_frames(self):

        valuesL = []
        for i in range(0, len(self.yes_valuesL), 2):

            startingBound = self.yes_valuesL[i]
            upperBound = self.yes_valuesL[i+1]
            print startingBound
            print upperBound
            valuesL += range(startingBound, upperBound)

        return valuesL

    def __repr__(self):
        return "No. of rows: %s" % len(self.data_file)

def flipFrameIdentities(dataFrame):
    dataFrameCopy = dataFrame.copy()
    dataFrameCopy.iloc[0, 2:] = dataFrame.iloc[1, 2:]
    dataFrameCopy.iloc[1, 2:] = dataFrame.iloc[0, 2:]
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

# trying class
a = CorrectCollisions(raw_data, results, rle)
