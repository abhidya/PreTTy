#Primary GUI display for preTTY
import tkinter as tk
import gui
import PreTTY
import balls
"""
Stitches together the multiple modules to
run the program. (May be replaced later on)
"""
if __name__ == "__main__":
    #Get initial directory and stats
    initial_dir = PreTTY.setup(PreTTY.start_up())
    tempArray = PreTTY.SizeScaler.get_percentiles()
    percentiles = tempArray[0]
    graveyardFiles = tempArray[1]

    #Start GUI
    root = tk.Tk()
    gui = gui.app(root)

    #Render center canvas
    center_display = balls.create_balls(root)
    center_display.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    #Print current directory to left hand display
    for k, v in initial_dir:
        gui.append_text(gui.left_window, str(v) + ": " + str(PreTTY.os.path.basename(k)) + "\n")

    #Render current dir files to canvas
    balls.update_ball_gui(center_display,percentiles)


    for k in graveyardFiles:
        print(str(k))
        gui.append_text(gui.right_window, str(k) + "\n")

    root.mainloop()