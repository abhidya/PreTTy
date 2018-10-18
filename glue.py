#Primary GUI display for preTTY
import tkinter as tk
import gui
import PreTTY

if __name__ == "__main__":
    initial_dir = PreTTY.setup(PreTTY.start_up())
    percentiles = PreTTY.SizeScaler.get_percentiles()

    #print(percentiles)
    #PreTTY.balls.ball_gui(percentiles)
    root = tk.Tk()
    gui = gui.app(root)

    for k, v in initial_dir:
        gui.append_text(gui.left_window, str(v) + ": " + str(PreTTY.os.path.basename(k)) + "\n")

    #Print given text to specified window
    #gui.update_text(gui.left_window,"Hello world!")
    #gui.update_text(gui.right_window,"Hello world!")

    #Clear text from window
    #gui.clear_text(gui.lefclt_window)

    #Append text to window
    #gui.append_text(gui.left_window, "Extra text!")

    root.mainloop()
