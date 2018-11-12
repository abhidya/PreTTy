import pickle
import os
import os.path
import time
import math
import sys
import Graveyard

# Opens a pickle file and returns a dictionary with the data
def openPickle(fileName):
    try:
        pklFile = open(fileName, "rb")
    except:
        print("Pickle file " + fileName + " could not be opened for reading\nFunction openPickle(), line 10 in Points_bcknd.py")
        #exit(1)
    files = pickle.load(pklFile)
    pklFile.close()
    return files


# Opens pickle file and parses the data.  Returns a dictionary 
# keyed on filename with points as the value
def parsePickle():
    pklFileName = "points.pkl"
    files = openPickle(pklFileName)
    pointsDict = {}
    graveyardDict = {}
    for file in files:
        if files[file] == 0:  # If a file belongs in the graveyard,
            graveyardDict[file] = os.path.getatime(file)  # Add it to the graveyard dictionary
    dictArray = [files, graveyardDict]
    return dictArray


def initPickle(directory):
    pklFileName = "points.pkl"
    pklFile = open(pklFileName, "wb")
    fileList = os.listdir(directory)
    fileList[:] = [directory + file for file in fileList]
    for file in fileList:
        print(file)
    points = {}
    minTime = sys.maxsize
    totalPoints = 0
    files = {}
    for file in files:
        print(file)
        files[file] = os.path.getatime(file)
        if files[file] < minTime:
            minTime = files[file]
        for file, point in files.items():
            if Graveyard.checkTime(file) == 1:
                points[file] = 0
                continue
            pointValue = math.ceil((points - minTime) / 604800)
            points[file] = pointValue
            totalPoints += pointValue
    points[directory] = totalPoints
    pickle.dump(points, pklFile)
    pklFile.close()


# Adds a point to the given filename
# Call this in frontend modules and pass it the filename
def addPoint(fileName):

    pklFileName = "points.pkl"
    files = openPickle(pklFileName)
    directory = os.path.dirname(pklFileName)
    files[directory] += 1
    files[fileName] += 1
    new_point = files[fileName]
    print(fileName + " incremented to " + str(new_point))
    with open(pklFileName, "wb") as pkl:
        pickle.dump(files, pkl)


    """for file in files:
        if files[file] > max:
            max = files[file]

    # print(max)
    files[fileName] = max +1  # Increment point by 1 for the click

    n = 1
    for key in sorted(files, key=files.get):
        files[key] = n
        n= n+1
    print(fileName + " incremented to max")
    with open(pklFileName, "wb") as pkl:
        pickle.dump(files, pkl)"""

