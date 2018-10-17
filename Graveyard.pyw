import os, time
import balls, SizeScaler

def checkTime(fileName):
	if os.path.getatime(fileName) < (time.time() - 35400000): #35400000 seconds in a year
		return 1
	else:
		return 0

def loadGraveyard(canvasArr):
	canvas = canvasArr[1]
	canvas.delete("all")
	percentiles = SizeScaler.get_percentiles(1)
	balls.ball_gui(percentiles, canvasArr)



