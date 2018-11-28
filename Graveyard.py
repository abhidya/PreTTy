import os, time
import balls, SizeScaler

timeframe = 35400000

def initGraveyard(time, type):
    global timeframe
    if type == "Day(s)":
        timeframe = time * 3600
    elif type == "Week(s)":
        timeframe = time * 604800
    elif type == "Month(s)":
        timeframe = time * (604800 * 4)
    elif type == "Year(s)":
        timeframe = time * 35400000

#Returns 1 if the file belongs in the graveyard
def checkTime(fileName):
    global timeframe
    try:
        #if os.path.getatime(fileName) < (time.time() - (604800 * 16)): #35400000 seconds in a year,  604800 seconds in a week, currently set to ~4 months
        if os.path.getatime(fileName) < (time.time() - (timeframe)): #35400000 seconds in a year,  604800 seconds in a week, currently set to ~4 months
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



