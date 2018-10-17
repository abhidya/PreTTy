import os, time
import balls, SizeScaler

def checkTime(fileName):
	if os.path.getatime(fileName) < (time.time() - (35400000)): #2628000 seconds in a month, 3.54e7 in a year
		return 1
	else:
		return 0

def loadGraveyard(canvasArr):
	canvas = canvasArr[1]
	canvas.delete("all")
	percentiles = SizeScaler.get_percentiles(1)
	balls.ball_gui(percentiles, canvasArr)



