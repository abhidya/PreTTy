import configparser
import os
import gui as GUI

import pickle
import platform
import balls
import SizeScaler
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

    filepath = " "

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
# It returns it as a dictionary (Filepath -> key, freq  -> value
def directory_initialize(directory_path):
    list_of_files = os.listdir(directory_path)
    list_of_files[:] = [directory_path + file for file in list_of_files]
    list_of_files = sorted(list_of_files, key=os.path.getctime)
    directory_dict = {}
    max_freq = len(list_of_files)
    for file in list_of_files:
        print(str(max_freq) + " :    " + file)
        directory_dict[file] = max_freq
        max_freq = max_freq - 1
    return directory_dict


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

        config.set('information', 'starting_directory',
                   str(path))  # writes new config settings
        config.set('information', 'initialized', 'True')
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        directory_dict = directory_initialize(path)
        # write python dict to a file
        try:
            output = open('freq_dict.pkl', 'wb')
            pickle.dump(directory_dict, output)
            output.close()
        except:
            print("Unable to write to file freq_dict.pkl")
            exit()
    config.read("config.ini")
    starting_directory = config.get("information", "starting_directory")

    return starting_directory


def setup(directory_path):
    # read python dict back from the file
    pkl_file = open('freq_dict.pkl', 'rb')
    allpaths = pickle.load(pkl_file)
    pkl_file.close()
    list_of_files = os.listdir(directory_path)
    directory_dict = {}
    unadded_to_dict = []
    for file in list_of_files:
        file = directory_path + file
        if file in allpaths:
            directory_dict[file] = allpaths[file]
        else:
            unadded_to_dict.append(file)
    if len(list_of_files) == len(unadded_to_dict):
        directory_dict = directory_initialize(directory_path)
        pkl_file = open('freq_dict.pkl', 'rb+')
        allpaths = pickle.load(pkl_file)
        allpaths.update(directory_dict)
        pkl_file.close()
        try:
            output = open('freq_dict.pkl', 'wb')
            pickle.dump(allpaths, output)
            output.close()
        except:
            print("Unable to write to file freq_dict.pkl")
            exit()
    s = [(k, directory_dict[k])
         for k in sorted(directory_dict, key=directory_dict.get, reverse=True)]

    return s


def command_parse(command):
    command_ls = command.split(' ')
    call(['ls'])


"""
Stitches together the multiple modules to
run the program. (May be replaced later on)
"""


def main(path):
    # Get initial directory and stats as well as graveyard files
    initial_dir = setup(path)
    # tempArray[0] is normal file percentiles and tempArray[1] is graveyard files
    tempArray = SizeScaler.get_percentiles()
    percentiles = tempArray[0]
    graveyardFiles = tempArray[1]

    # Uncomment this in order to create a dictionary of all files not in the graveyard
    nonGraveyardFiles = {}
    for i, j in percentiles.items():
        if i in graveyardFiles:
            continue

        for item in initial_dir:
            # print(i, item[0])
            if i == item[0]:
                nonGraveyardFiles[i] = j

    # Start GUI
    root = tk.Tk()
    try:
        root.state("zoomed")
    except:
        pass

    gui = GUI.app(root)

    # Render center canvas
    #center_display = balls.create_balls(gui.canvas_frame)
    
    #center_display.pack()
    #gui.canvas_frame.pack()
    # myframe = tk.Frame(center_display)
    # myframe.pack(fill="both", expand=True)
    #

    #gui.canvas_frame.place(relx=.5, rely=.5, anchor=tk.CENTER,)

    # Print current directory to left hand display
    if len(initial_dir) == 0:  # If all files belong in the graveyard
        gui.append_text(gui.left_window, "All files in graveyard!")
    for k, v in initial_dir:
        if k in graveyardFiles:  # If a file is in the graveyard, don't print it to the left window
            continue
        gui.append_text(gui.left_window, str(os.path.basename(k)) + "\n")

    # Render current dir files to canvas
    balls.update_ball_gui(gui.canvas, nonGraveyardFiles, root, gui)

    # Print graveyard files on the right window
    if len(graveyardFiles) == 0:  # If there are no graveyard files
        gui.append_text(gui.right_window, "No graveyard files!")
    for k in graveyardFiles:
        gui.append_text(gui.right_window, str(os.path.basename(k)) + "\n")

    # Print out help window
    gui.append_text(gui.middle_window,
                    "Welcome to PreTTy 1.0! \n\nThis program allows you to visualize your files in a more effective way. \n\nShortcuts: \n \nf = view files \nw = quit program \nh = help window \ng = view graveyard \n\nCreated by Manny Bhidya, Hayden Coffey, Nathan Johnson, Cody Lawson, and Cara Scott \n \nStill have problems? Email Hayden.")

    #gui.setcanvas(center_display)
    root.mainloop()
