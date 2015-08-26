

import os
import sys
from position_validate import results_file
from configurations  import validation_results_dir
import pandas as pd
import inspect
import numpy as np
ee = execfile
import matplotlib.pyplot as plt
import pdb
poing = inspect.getabsfile(inspect.currentframe())
from configurations import col_names, data_dir

file_path = os.path.join(validation_results_dir, results_file) 

print file_path


curated = pd.read_csv(file_path, names=col_names[:4])
generatedFilePathS = os.path.join(data_dir,"data_shortcoll.csv")
generated = pd.read_csv(generatedFilePathS, names=col_names)

xL = []
curated_x = []
generated_x = []

curated_y = []
generated_y = []

for row in curated.values:

    frame_number = row[0] # getting the frame number in the curated row
    fly_number = row[1] # getting the fly string in the curated row

    # getting the appropriate match in the values.
    values = generated[generated.frame_number == frame_number]

    for i in values.values:
        if i[1] == fly_number:
            row_in_generated = i
            break

    if abs(row_in_generated[2] - row[2]) > 5:
        print row_in_generated
        print row
    generated_x.append(row_in_generated[2])
    curated_x.append(row[2])
    generated_y.append(row_in_generated[3])
    curated_y.append(row[3])


# do linear regression
def plotWithBestFitLine(xL, yL, outputFileNameS):
    xL = np.array(xL)
    yL = np.array(yL)
    m, b = np.polyfit(xL, yL, 1)

    # plotting both scatter plot and linear regression
    plt.scatter(xL, yL)
    plt.plot(xL, m*xL+b, '-r')
    plt.xlabel("generated x-coordinates")
    plt.ylabel("manually inspected x-coordinates    ")
    plt.savefig(outputFileNameS)
    plt.show()
    return m, b

m, b = plotWithBestFitLine(generated_x, curated_x, "xlinreg.png")
m, b = plotWithBestFitLine(generated_y, curated_y, "ylinreg.png")
