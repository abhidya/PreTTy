import pickle
import os
import time
import math
import sys
import Graveyard
#Opens a pickle file and returns a dictionary with the data
def openPickle(fileName):
    pklFile = open(fileName, "rb")
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
	minTime = sys.maxsize
	for file in files: 
		if Graveyard.checkTime(file) == 1:
			graveyardDict[file] = os.path.getatime(file)
		else:
			files[file] = os.path.getatime(file)	#Get the last time the file was accessed
		if files[file] < minTime:				#If the file was accessed less recently than another file, store this
                           				#timestamp
			minTime = files[file]
	for file, points in files.items():			#Files get 1 point for every week their getatime() is past the least
		pointValue = math.ceil((points - minTime) / 604800) #Seconds in a week
		pointsDict[file] = pointValue
		if file in graveyardDict:
			graveyardDict[file] = pointValue
	with open("points.pkl", "wb") as pkl:
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