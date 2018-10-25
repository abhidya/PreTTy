import configparser
import os
import pickle
import platform
import balls
import SizeScaler

# from theFace import app
#
# import gi
# # Painful installation, used for get_thumbnail() . i followed them making a symbolic link: https://askubuntu.com/questions/1057832/how-to-install-gi-for-anaconda-python3-6
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gio, Gtk


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


def get_thumbnail(filename, size):
    # This is temporary need to generate better thumbnails.
    # https://stackoverflow.com/questions/25511706/get-associated-filetype-icon-for-a-file or
    # https://github.com/FelixSchwarz/anythumbnailer  or
    # we do our own!

    pass
    #final_filename = ""
    #if os.path.exists(filename):
    #    file = Gio.File.new_for_path(filename)
    #    info = file.query_info('standard::icon', 0, Gio.Cancellable())
    #    icon = info.get_icon().get_names()[0]
    #
    #        icon_theme = Gtk.IconTheme.get_default()
    #        icon_file = icon_theme.lookup_icon(icon, size, 0)
    #        if icon_file != None:
    #            final_filename = icon_file.get_filename()
    #        return final_filename


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

    s = [(k, directory_dict[k])
         for k in sorted(directory_dict, key=directory_dict.get, reverse=True)]

    return s
