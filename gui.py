import tkinter as tk
import sys
import math
import PreTTY
"""
Code for class based GUI object.
"""


class app(object):
    def __init__(self, parent):
        #Background and foreground colors
        bg_c = "black"
        fg_c = "white"

        #Designate root window
        self.root = parent
        self.root.title("preTTy")

        #Calculates screen size and centers window position
        # Get screen width [pixels]
        ScreenSizeX = self.root.winfo_screenwidth()
        # Get screen height [pixels]
        ScreenSizeY = self.root.winfo_screenheight()
        # Set the screen ratio for width and height
        ScreenRatio = 1.0
        FrameSizeX = int(ScreenSizeX * ScreenRatio)
        FrameSizeY = int(ScreenSizeY * ScreenRatio)
        # Find left and up border of window
        FramePosX = int(math.ceil((ScreenSizeX - FrameSizeX)/2))
        FramePosY = int(math.ceil((ScreenSizeY - FrameSizeY)/2))
        self.root.geometry("%sx%s+%s+%s" %
                           (FrameSizeX, FrameSizeY, FramePosX, FramePosY))

        #self.root.geometry("1200x750")
        self.root.configure(background=bg_c)

        #Hot keys
        self.root.bind_all("<Control-w>", self.quit)
        self.root.bind_all("<Control-f>", self.toggle_left)
        self.root.bind_all("<Control-h>", self.toggle_right)

        #Toggle switches
        self.theme_bool = 0
        self.left_bool = 0
        self.right_bool = 0

        #Frame to hold prompt and left display toggle
        self.prompt_frame = tk.Frame(self.root, bg=bg_c)

        #Text Frames
        self.left_txt_frame = tk.Frame(self.root, bg=bg_c)
        self.right_txt_frame = tk.Frame(self.root, bg=bg_c)

        self.prompt_frame.pack(side=tk.BOTTOM)

        #Application title displayed on window
        self.app_logo = tk.PhotoImage(file="graphics/logo_light.gif")
        self.app_logo = self.app_logo.subsample(2, 2)
        self.app_name = tk.Label(
            self.root, image=self.app_logo, bg=bg_c, fg=fg_c)

        self.app_name.pack(side=tk.TOP)

        #Left Hand Text Display (File Directory)
        #TODO: Change this to be interactive, clickable
        self.left_window = tk.Text(
            self.left_txt_frame, width=40, height=60, wrap=tk.WORD, bg=bg_c, fg=fg_c)
        self.left_window.grid(row=0, column=0, sticky='nsew')

        #Left scroll bar
        leftScrollbr = tk.Scrollbar(
            self.left_txt_frame, command=self.left_window.yview)
        leftScrollbr.grid(row=0, column=1, sticky='nsew')
        self.left_window['yscrollcommand'] = leftScrollbr.set

        #Right Hand Text Display (Graveyard)
        self.right_window = tk.Text(
            self.right_txt_frame, width=40, height=60, wrap=tk.WORD, bg=bg_c, fg=fg_c)
        self.right_window.grid(row=0, column=0, sticky='nsew')

        #Right scroll bar
        rightScrollbr = tk.Scrollbar(
            self.right_txt_frame, command=self.right_window.yview)
        rightScrollbr.grid(row=0, column=1, sticky='nsew')
        self.right_window['yscrollcommand'] = rightScrollbr.set

        #Buttons to hide and show text display
        self.left_display_button = tk.Button(
            self.prompt_frame, text="File View", command=self.toggle_left)
        self.left_display_button.grid(row=0, column=0)

        #Buttons to hide and show Graveyard display
        self.right_display_button = tk.Button(
            self.prompt_frame, text="Graveyard", command=self.toggle_right)
        self.right_display_button.grid(row=1, column=0)

        #Command prompt
        #TODO: Add hotkey to set focus easily
        e = tk.Entry(self.prompt_frame, width=25)
        e.focus()
        e.bind('<Return>', self.get)
        e.grid(row=3, column=0)

        #Light / Dark theme toggle button
        self.theme_button = tk.Button(
            self.root, text="Theme", command=self.theme_toggle)

        self.theme_button.pack(side=tk.BOTTOM)

    #Replace contents of text window with data
    def update_text(self, window, data):
        window.config(state=tk.NORMAL)
        window.delete(0.0, tk.END)
        window.insert(tk.END, data)
        window.config(state=tk.DISABLED)

    #Clear contents of text window
    def clear_text(self, window):
        window.delete(0.0, tk.END)

    #Append given data to current data in text window
    def append_text(self, window, data):
        window.config(state=tk.NORMAL)
        window.insert(tk.END, data)
        window.config(state=tk.DISABLED)

    #pulls text from given text widget
    def get(self, event):
        #self.update_text(self.left_window, event.widget.get())
        PreTTY.command_parse(event.widget.get())
        event.widget.delete(0, tk.END)

    #Toggle left hand display
    def toggle_left(self, event=''):
        if(self.left_bool):
            self.left_txt_frame.pack_forget()
        else:
            self.left_txt_frame.pack(side=tk.LEFT)

        self.left_bool = (self.left_bool + 1) % 2

    #Toggle right hand display
    def toggle_right(self, event=''):
        if(self.right_bool):
            self.right_txt_frame.pack_forget()
        else:
            self.right_txt_frame.pack(side=tk.RIGHT)

        self.right_bool = (self.right_bool + 1) % 2

    #TODO: Optimize this so function does not become too big
    #Toggle between light and dark themes
    def theme_toggle(self):
        if(self.theme_bool):
            #dark theme
            self.root.config(bg="black")
            self.prompt_frame.config(bg="black")
            self.left_window.config(bg="black", fg="white")
            self.right_window.config(bg="black", fg="white")

            #Application title displayed on window
            self.app_name.pack_forget()
            self.app_logo = tk.PhotoImage(file="graphics/logo_light.gif")
            self.app_logo = self.app_logo.subsample(2, 2)
            self.app_name = tk.Label(
                self.root, image=self.app_logo, bg="black")

            self.app_name.pack(side=tk.TOP)

        else:
            #white theme
            self.root.config(bg="white")
            self.prompt_frame.config(bg="white")
            self.left_window.config(bg="white", fg="black")
            self.right_window.config(bg="white", fg="black")

            #Application title displayed on window
            self.app_name.pack_forget()
            self.app_logo = tk.PhotoImage(file="graphics/logo.gif")
            self.app_logo = self.app_logo.subsample(2, 2)
            self.app_name = tk.Label(
                self.root, image=self.app_logo, bg="white")

            self.app_name.pack(side=tk.TOP)

        self.theme_bool = (self.theme_bool + 1) % 2

    #Close app
    def quit(self, event):
        sys.exit(0)
