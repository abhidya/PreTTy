#Primary GUI display for preTTY
import tkinter as tk
import gui
import PreTTY
import balls

if __name__ == "__main__":
    #Get initial directory and stats
    initial_dir = PreTTY.setup(PreTTY.start_up())
    percentiles = PreTTY.SizeScaler.get_percentiles()

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

    root.mainloop()