import tkinter as tk
import gui
import PreTTY
import balls

"""
Stitches together the multiple modules to
run the program. (May be replaced later on)
"""

if __name__ == "__main__":
    #Get initial directory and stats as well as graveyard files
    initial_dir = PreTTY.setup(PreTTY.start_up())
    # tempArray[0] is normal file percentiles and tempArray[1] is graveyard files
    tempArray = PreTTY.SizeScaler.get_percentiles()
    percentiles = tempArray[0]
    graveyardFiles = tempArray[1]

    #Uncomment this in order to create a dictionary of all files not in the graveyard
    nonGraveyardFiles = {}
    for i, j in percentiles.items():
        if i in graveyardFiles:
            continue
        nonGraveyardFiles[i] = j

    #Start GUI
    root = tk.Tk()
    try:
        root.state("zoomed")
    except:
        pass

    gui = gui.app(root)

    #Render center canvas
    center_display = balls.create_balls(root)
    center_display.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    #Print current directory to left hand display
    if len(initial_dir) == 0:  # If all files belong in the graveyard
        gui.append_text(gui.left_window, "All files in graveyard!")
    for k, v in initial_dir:
        if k in graveyardFiles:  # If a file is in the graveyard, don't print it to the left window
            continue
        gui.append_text(gui.left_window, str(PreTTY.os.path.basename(k)) + "\n")

    #Render current dir files to canvas
    balls.update_ball_gui(center_display, percentiles)

    #Print graveyard files on the right window
    if len(graveyardFiles) == 0:  # If there are no graveyard files
        gui.append_text(gui.right_window, "No graveyard files!")
    for k in graveyardFiles:
        gui.append_text(gui.right_window, str(PreTTY.os.path.basename(k)) + "\n")

    #Print out help window
    gui.append_text(gui.middle_window, "Welcome to PreTTy 1.0! \n\nThis program allows you to visualize your files in a more effective way. \n\nShortcuts: \n \nf = view files \nw = quit program \nh = help window \ng = view graveyard \n\nCreated by Manny Bhidya, Hayden Coffey, Nathan Johnson, Cody Lawson, and Cara Scott \n \nStill have problems? Email Hayden.")

    root.mainloop()
