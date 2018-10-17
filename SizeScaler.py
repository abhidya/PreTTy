import math
import Points_bcknd

"""
Code for scaling points to icon sizes
Use either percentiles or distribution
"""


#returns dictionary keyed by file name to percentile its points are in
def get_percentiles():
    #dictionary keyed on file names read from pickle file
    file_and_points = Points_bcknd.parsePickle()
    if len(file_and_points) == 0:
        print("bad pickle\n")
    total_points = 0

    for file in file_and_points:
        total_points = total_points + file_and_points[file]


    mu = total_points/len(file_and_points)

    sum_of_differences = 0

    for file in file_and_points:
        sum_of_differences = sum_of_differences + (file_and_points[file] - mu)**2

    sdeviation = math.sqrt(sum_of_differences/len(file_and_points))
    if sdeviation == 0:
        sdeviation = 0.0001
    #print("average: " + str(mu) + "\n" + "SD: " + str(sdeviation) + "\n")
    zscores = {}

    for file in file_and_points:
        zscores[file] = (file_and_points[file] - mu)/sdeviation
        #print(file + ": " + str(zscores[file]))
        if len(zscores) == 0:
            print("fuckin empty bro\n")

    percentiles = {}
    for file in zscores:
        if zscores[file] >= 1.6:
            percentiles[file] = 5
        elif zscores[file] >= 1 and zscores[file] < 1.6:
            percentiles[file] = 4
        elif zscores[file] < 1 and zscores[file] >= 0:
            percentiles[file] = 3
        elif zscores[file] < 0 and zscores[file] >= -1:
            percentiles[file] = 2
        elif zscores[file] < -1:
            percentiles[file] = 1
        #print(file + ": " + str(percentiles[file]))

    return percentiles

#get_percentiles()








