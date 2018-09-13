import configparser
import glob
import pickle

import os
from tkinter import filedialog as fd



import gi
# Painful installation, used for get_thumbnail() . i followed them making a symbolic link: https://askubuntu.com/questions/1057832/how-to-install-gi-for-anaconda-python3-6
gi.require_version('Gtk', '3.0')
from gi.repository import Gio , Gtk
import tkinter as tk



class Prompt(tk.Tk):

    filepath =" "
    def BrowseButtonClickOutput(self):
        """
        Browse button for choosing output dir
        """
        mydir = fd.askdirectory(initialdir=" //network/folder/", mustexist=True)

        self.filepath = mydir
        self.label["text"] = self.filepath

    def __init__(self):
        self.answer = None
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text=self.filepath)
        self.button = tk.Button(self, text="Confirm", command=self.on_button)
        self.browsebuttonOutput = tk.Button(self, text=u"Browse...",command=self.BrowseButtonClickOutput)

        self.browsebuttonOutput.pack()
        self.button.pack()
        self.label.pack()

    def on_button(self):
        self.answer = self.filepath
        self.quit()

def get_thumbnail(filename,size):

    # This is temporary need to generate better thumbnails.
    # maybe https://pypi.org/project/preview-generator/0.2.2/   or
    # https://stackoverflow.com/questions/25511706/get-associated-filetype-icon-for-a-file or
    # https://github.com/FelixSchwarz/anythumbnailer  or
    # we do our own!


    final_filename = ""
    if os.path.exists(filename):
        file = Gio.File.new_for_path(filename)
        info = file.query_info('standard::icon' , 0 , Gio.Cancellable())
        icon = info.get_icon().get_names()[0]

        icon_theme = Gtk.IconTheme.get_default()
        icon_file = icon_theme.lookup_icon(icon , size , 0)
        if icon_file != None:
            final_filename = icon_file.get_filename()
        return final_filename



def directory_initialize(directory_path):
    list_of_files = glob.glob(directory_path)  # * means all if need specific format then *.csv
    list_of_files = sorted(list_of_files, key=os.path.getctime)
    directory_dict = {}
    max_freq = len(list_of_files)
    for file in list_of_files:
        # print(str(max_freq) + " :    " + file)
        directory_dict[file] = max_freq
        max_freq= max_freq -1
    return directory_dict


def start_up():

    config = configparser.ConfigParser()
    config.read("config.ini")
    initialized = config.get("information", "initialized")

    if(initialized == "false"):

        # Implement GUI window to ask for path to desktop and return string
        # path = GUI_desktop_path()

        # path = input("Path to Desktop?: (ex: /home/manny/Desktop/ )" + '\n')

        promptData = Prompt()
        promptData.mainloop()
        promptData.destroy()
        path = promptData.filepath
        path = path+"/"

        config.set('information', 'starting_directory', str(path))
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



    # directory_initialize(starting_directory + "*")
    # return directory_initialize(starting_directory + "*")

    return starting_directory



def mvc(filepath):
    root = tk.Tk()

    w2 = tk.Label(root, justify=tk.LEFT, padx=10,
                  text=filepath).pack(side="left")
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
        filename = k.replace('/home/manny/Desktop/', '')
        print(str(v) + ": " + str(filename) + "\n")

        # print(mvc(get_thumbnail(k, 50)))




setup(start_up())


