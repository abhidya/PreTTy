import math
import Points_bcknd

"""
Code for scaling points to icon sizes
Use either percentiles or distribution
"""


#returns an array with index 0 being dictionary keyed by file name to percentile its points are in and index 1 being the graveyard files
#Pass True if points.pkl is expected to have points associated with the directory; false otherwise
def get_percentiles():
    #dictionary keyed on file names read from pickle file
    tempArray = Points_bcknd.parsePickle()
    file_and_points = tempArray[0]      #Contains all files and point values
    graveyard_files = tempArray[1]      #Contains only graveyard files
    if len(file_and_points) == 0:      #Possibly all files could be in the graveyard so this isn't needed
        return tempArray
    total_points = 0

    for file in file_and_points:
        total_points = total_points + file_and_points[file]

    mu = total_points/len(file_and_points)

    sum_of_differences = 0

    for file in file_and_points:
        sum_of_differences = sum_of_differences + (file_and_points[file] - mu)**2

    sdeviation = math.sqrt(sum_of_differences/len(file_and_points))
    if sdeviation == 0:
        sdeviation = 0.00001
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
    tempArray = [percentiles, graveyard_files]
    return tempArray

#get_percentiles()








