import configparser
import os
import gui as GUI

import pickle
import platform
import balls
import SizeScaler
import Points_bcknd as points
from subprocess import call

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox


def createConfig():
    config = configparser.ConfigParser()
    config["information"] = {"initialized": "false",
                             "starting_directory": "", "freq_dict": "freq_dict.pkl"}
    with open("config.ini", "w") as configfile:
        config.write(configfile)


class MVC(tk.Tk):  # Model View Controller

    filepath = ""

    # String that holds file path of desktop given by user

    def BrowseButtonClickOutput(self):
        """
        Browse button for choosing Desktop Directory
        """
        mydir = fd.askdirectory(mustexist=True)

        self.filepath = mydir
        self.label["text"] = self.filepath

    #     Updates label with directory chosen to allow user to confirm

    def __init__(self):
        self.answer = None
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="Path to your Desktop Folder.")
        self.button = tk.Button(self, text="Confirm", command=self.on_button)
        self.browsebuttonOutput = tk.Button(
            self, text=u"Browse...", command=self.BrowseButtonClickOutput)
        self.title("preTTY")
        self.configure(background="black")

        app_name = tk.Label(self, text="preTTY", bg="black",
                            fg="white", font="none 24 bold")
        app_name.pack(side=tk.TOP)
        self.browsebuttonOutput.pack(side=tk.RIGHT)
        self.button.pack(side=tk.RIGHT)
        self.label.pack(side=tk.LEFT)
        self.geometry("400x300")

    #     GUI for choosing directory

    def on_button(self):
        self.answer = self.filepath
        try:
            os.listdir(self.filepath)
            self.quit()
        except:
            messagebox.showinfo("Error", "Please choose a valid path")


# Given a new directory this will sort the files by date used and assign them frequency numbers
# It returns it as a dictionary (Filepath -> key, freq  -> value)

def start_up():
    # Reads Config file, does first time start up logid

    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        initialized = config.get("information", "initialized")
    except:
        createConfig()
        config.read("config.ini")
        initialized = config.get("information", "initialized")

    if (initialized != "True"):  # if this is the first run, ask for desktop path

        promptData = MVC()
        promptData.mainloop()
        promptData.destroy()
        path = promptData.filepath
        path = path + "/"

        config.set('information', 'starting_directory', str(path))  # writes new config settings
        config.set('information', 'initialized', 'True')
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        points.initPickle(path)

    config.read("config.ini")
    starting_directory = config.get("information", "starting_directory")
    temp = SizeScaler.get_percentiles(starting_directory)
    dictArray = [starting_directory, temp]

    return dictArray

def command_parse(command):
    command_ls = command.split(' ')
    call(['ls'])


"""
Stitches together the multiple modules to
run the program. (May be replaced later on)
"""


def main(dictArray):
    # Get initial directory and stats as well as graveyard files
    path = dictArray[0]
    # tempArray[0] is normal file percentiles and tempArray[1] is graveyard files
    tempArray = dictArray[1]
    percentiles = tempArray[0]
    graveyardFiles = tempArray[1]

    # Uncomment this in order to create a dictionary of all files not in the graveyard
    nonGraveyardFiles = {}
    for i, j in percentiles.items():
        if i in graveyardFiles:
            continue
        nonGraveyardFiles[i] = j

    # Start GUI
    root = tk.Tk()
    try:
        root.state("zoomed")
    except:
        pass
    gui = GUI.app(root)
    gui.root = root
    gui.desktoppath = path
    gui.backhistory = path

    # Render center canvas
    #center_display = balls.create_balls(gui.canvas_frame)
    
    #center_display.pack()
    #gui.canvas_frame.pack()
    # myframe = tk.Frame(center_display)
    # myframe.pack(fill="both", expand=True)
    #

    #gui.canvas_frame.place(relx=.5, rely=.5, anchor=tk.CENTER,)

    # Print current directory to left hand display
    if len(nonGraveyardFiles) == 0:  # If all files belong in the graveyard
        gui.append_text(gui.left_window, "All files in graveyard!")
    else:
        for k in nonGraveyardFiles:
            gui.append_text(gui.left_window, str(os.path.basename(k)) + "\n")

    # Render current dir files to canvas
    balls.update_ball_gui(gui.canvas, nonGraveyardFiles, root, gui)

    # Print graveyard files on the right window
    if len(graveyardFiles) == 0:  # If there are no graveyard files
        gui.append_text(gui.right_window, "No graveyard files!")
    else:
        for k in graveyardFiles:
            gui.append_text(gui.right_window, str(os.path.basename(k)) + "\n")

    # Print out help window
    f = open('instructions.txt', 'r')
    file_contents = f.read()
    gui.append_text(gui.help_window, file_contents)
    f.close()

    #gui.setcanvas(center_display)
    root.mainloop()
