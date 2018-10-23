import pickle
import os
import time
import math
import sys
import Graveyard


#Opens a pickle file and returns a dictionary with the data
def openPickle(fileName):
    try:
        pklFile = open(fileName, "rb")
    except:
        print("Pickle file "+fileName+" could not be opened for reading\nFunction openPickle(), line 10 in Points_bcknd.py")
        exit(1)
    files = pickle.load(pklFile)
    pklFile.close()
    return files

#Opens pickle file and parses the data.  Returns a dictionary keyed on filename
#with points as the value
def parsePickle():
	pklFileName = "freq_dict.pkl"
	files = openPickle(pklFileName)
	pointsDict = {}
	graveyardDict = {}
	minTime = sys.maxsize       #Set initial value so any other values are guaranteed to be smaller
	for file in files: 
		if Graveyard.checkTime(file) == 1:      #If a file belongs in the graveyard,
			graveyardDict[file] = os.path.getatime(file)        #Add it to the graveyard dictionary
		else:
			files[file] = os.path.getatime(file)	#Get the last time the file was accessed
			if files[file] < minTime:				#If the file was accessed less recently than another file, store this
			    minTime = files[file]
	for file, points in files.items():			#Files get 1 point for every week their getatime() is past the smallest least recently accessed file
		pointValue = math.ceil((points - minTime) / 604800) #Seconds in a week
		pointsDict[file] = pointValue
		if file in graveyardDict:           #Set point values in graveyard dict
			graveyardDict[file] = pointValue
	with open("points.pkl", "wb") as pkl:       #Write these values to the points pkl file
		pickle.dump(pointsDict, pkl)
	dictArray = [pointsDict, graveyardDict]
	return dictArray

#Adds a point to the given filename
#Call this in frontend modules and pass it the filename
def addPoint(fileName):
	pklFileName = "points.pkl"
	files = openPickle(pklFileName)
	files[fileName] = files[fileName] + 1		#Increment point by 1 for the click
	path_lists = fileName.split('/')
	path_lists.reverse()
	file2 = path_lists[0]
	print(file2 + " incremented to " + str(files[fileName]))
	with open(pklFileName, "wb") as pkl:
		pickle.dump(files, pkl)