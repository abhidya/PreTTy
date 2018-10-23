import os, time
import balls, SizeScaler

def checkTime(fileName):
    try:
        if os.path.getatime(fileName) < (time.time() - (604800 * 16)): #35400000 seconds in a year,  604800 seconds in a week, currently set to ~4 months
            return 1
        else:
            return 0
    except:
        print("Could not get atime for file "+fileName+"\nFunction checkTime(), line 4 in Graveyard.py")
        exit(1)

#Outdated function
def loadGraveyard(canvasArr):
	canvas = canvasArr[1]
	canvas.delete("all")
	percentiles = SizeScaler.get_percentiles(1)
	balls.ball_gui(percentiles, canvasArr)



