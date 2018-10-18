#Primary GUI display for preTTY
import tkinter as tk
import gui
import PreTTY
import balls

if __name__ == "__main__":
    initial_dir = PreTTY.setup(PreTTY.start_up())
    percentiles = PreTTY.SizeScaler.get_percentiles()

    #print(percentiles)
    root = tk.Tk()
    gui = gui.app(root)

    center_display = balls.create_balls(root)

    center_display.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    for k, v in initial_dir:
        gui.append_text(gui.left_window, str(v) + ": " + str(PreTTY.os.path.basename(k)) + "\n")

    balls.update_ball_gui(center_display,percentiles)
    #PreTTY.balls.update_ball_gui(percentiles)
    #Print given text to specified window
    #gui.update_text(gui.left_window,"Hello world!")
    #gui.update_text(gui.right_window,"Hello world!")

    #Clear text from window
    #gui.clear_text(gui.lefclt_window)

    #Append text to window
    #gui.append_text(gui.left_window, "Extra text!")

    root.mainloop()
