import configparser
import glob
import pickle
import os
from tkinter import filedialog as fd
import platform

import gi

# Painful installation, used for get_thumbnail() . i followed them making a symbolic link: https://askubuntu.com/questions/1057832/how-to-install-gi-for-anaconda-python3-6
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk
import tkinter as tk


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
        self.browsebuttonOutput = tk.Button(self, text=u"Browse...", command=self.BrowseButtonClickOutput)
        self.title("preTTY")
        self.configure(background="black")

        app_name = tk.Label(self, text="preTTY", bg="black", fg="white", font="none 24 bold")
        app_name.pack(side=tk.TOP)
        self.browsebuttonOutput.pack(side=tk.RIGHT)
        self.button.pack(side=tk.RIGHT)
        self.label.pack(side=tk.LEFT)
        self.geometry("400x300")

    #     GUI for choosing directory

    def on_button(self):
        self.answer = self.filepath
        self.quit()


def get_thumbnail(filename, size):
    # This is temporary need to generate better thumbnails.
    # maybe https://pypi.org/project/preview-generator/0.2.2/   or
    # https://stackoverflow.com/questions/25511706/get-associated-filetype-icon-for-a-file or
    # https://github.com/FelixSchwarz/anythumbnailer  or
    # we do our own!

    final_filename = ""
    if os.path.exists(filename):
        file = Gio.File.new_for_path(filename)
        info = file.query_info('standard::icon', 0, Gio.Cancellable())
        icon = info.get_icon().get_names()[0]

        icon_theme = Gtk.IconTheme.get_default()
        icon_file = icon_theme.lookup_icon(icon, size, 0)
        if icon_file != None:
            final_filename = icon_file.get_filename()
        return final_filename


def open_file(path):
    usersOS = platform.system()

    if (usersOS == "Linux"):
        os.system("xdg-open " + path)

    elif (usersOS == "Windows"):
        os.system("start" + filename)

    elif (usersOS == "Darwin"):
        os.system("open " + path)

    else:
        try:  # linux
            os.system("xdg-open " + path)
        except:
            pass
        try:  # Windows
            os.system("start" + filename)
        except:
            pass
        try:  # MacOS
            os.system("open " + path)
        except:
            pass


# Given a new directory this will sort the files by date used and assign them frequency numbers
# It returns it as a dictionary (Filepath -> key, freq  -> value
def directory_initialize(directory_path):
    list_of_files = glob.glob(directory_path)  # * means all if need specific format then *.csv
    list_of_files = sorted(list_of_files, key=os.path.getctime)
    directory_dict = {}
    max_freq = len(list_of_files)
    for file in list_of_files:
        # print(str(max_freq) + " :    " + file)
        directory_dict[file] = max_freq
        max_freq = max_freq - 1
    return directory_dict


def start_up():
    # Reads Config file, does first time start up logid

    config = configparser.ConfigParser()
    config.read("config.ini")
    initialized = config.get("information", "initialized")

    if (initialized == "false"):  # if this is the first run, ask for desktop path

        promptData = MVC()
        promptData.mainloop()
        promptData.destroy()
        path = promptData.filepath
        path = path + "/"

        config.set('information', 'starting_directory', str(path))  # writes new config settings
        config.set('information', 'initialized', 'True')
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        directory_dict = directory_initialize(path + "*")
        # write python dict to a file
        output = open('freq_dict.pkl', 'wb')
        pickle.dump(directory_dict, output)
        output.close()

    config.read("config.ini")
    starting_directory = config.get("information", "starting_directory")

    return starting_directory


def theFace(file_dictionary):
    # command is a string retrieved from text box
    def updateWindow(command=''):
        output.delete(0.0, tk.END)
        output.insert(tk.END, file_dictionary)

    def get(event):
        updateWindow(event.widget.get())

    root = tk.Tk()

    root.title("preTTY")
    root.configure(background="black")

    app_name = tk.Label(root, text="preTTY", bg="black", fg="white", font="none 12 bold")
    app_name.pack(side=tk.TOP)

    output = tk.Text(root, width=75, height=6, wrap=tk.WORD, background="white")
    output.pack(side=tk.BOTTOM)

    e = tk.Entry(root, width=25)
    e.bind('<Return>', get)
    e.pack(side=tk.BOTTOM)

    updateWindow()
    root.mainloop()


def setup(directory_path):
    # read python dict back from the file
    pkl_file = open('freq_dict.pkl', 'rb')
    allpaths = pickle.load(pkl_file)
    pkl_file.close()
    list_of_files = glob.glob(directory_path + "*")  # * means all if need specific format then *.csv

    directory_dict = {}
    unadded_to_dict = []
    for file in list_of_files:
        if file in allpaths:
            directory_dict[file] = allpaths[file]
        else:
            unadded_to_dict.append(file)

    s = [(k, directory_dict[k]) for k in sorted(directory_dict, key=directory_dict.get, reverse=True)]
    for k, v in s:
        print(str(v) + ": " + str(os.path.basename(k)) + "\n")

    open_file(max(directory_dict, key=directory_dict.get))
    theFace(sorted(directory_dict, key=directory_dict.get, reverse=True))


setup(start_up())
