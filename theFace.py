#Primary GUI display for preTTY
import tkinter as tk
import sys
from gui import app

if __name__ == "__main__":
    root = tk.Tk()
    gui = app(root)
    root.mainloop()
