#Primary GUI display for preTTY
import tkinter as tk
import sys
from gui import app

if __name__ == "__main__":
    root = tk.Tk()
    gui = app(root)

    #Print given text to specified window
    #gui.update_text(gui.left_window,"Hello world!")
    #gui.update_text(gui.right_window,"Hello world!")

    #Clear text from window
    #gui.clear_text(gui.left_window)

    #Append text to window
    #gui.append_text(gui.left_window, "Extra text!")

    root.mainloop()
