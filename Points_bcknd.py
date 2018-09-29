import pickle
import os, time, math, sys

def parsePickle():
	filename = "freq_dict.pkl"
	pkl_file = open(filename, 'rb')
	files = pickle.load(pkl_file)
	pkl_file.close()
	points_dict = {}
	minTime = sys.maxsize
	for file in files: 
		files[file] = os.path.getatime(file)
		if files[file] < minTime:
			minTime = files[file]
	for file, points in files.items():
		pointValue = math.ceil((points-minTime)/604800)
		print(file + ":  " + str(pointValue))
		points_dict[file] = pointValue
	return points_dict

parsePickle()



