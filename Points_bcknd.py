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
        print(
            "Pickle file " + fileName + " could not be opened for reading\nFunction openPickle(), line 10 in Points_bcknd.py")
        #exit(1)
    files = pickle.load(pklFile)
    pklFile.close()
    return files


# Opens pickle file and parses the data.  Returns a dictionary keyed on filename
# with points as the value
#Pass True if points.pkl is expected to have points associated with the directory; false otherwise
def parsePickle(triri):
    pklFileName = "freq_dict.pkl"
    if option == True:      #Config.ini has been initialized
        files = openPickle("points.pkl")
        graveyardDict = {}
        pointsDict = {}
        for file in files:
            print(str(file)+ " " + str(files[file]))
            if Graveyard.checkTime(file) == 1:
                graveyardDict[file] = os.path.getatime(file)
            else:
                pointsDict[file] = files[file]
        dictArray = [pointsDict, graveyardDict]
        return dictArray

    files = openPickle(pklFileName)
    pointsDict = {}
    graveyardDict = {}
    minTime = sys.maxsize  # Set initial value so any other values are guaranteed to be smaller
    for file in files:
        if Graveyard.checkTime(file) == 1:  # If a file belongs in the graveyard,
            graveyardDict[file] = os.path.getatime(file)  # Add it to the graveyard dictionary
    with open("points.pkl", "wb") as pkl:  # Write these values to the points pkl file
        pickle.dump(files, pkl)
    dictArray = [files, graveyardDict]
    return dictArray



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

