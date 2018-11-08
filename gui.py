import tkinter as tk
import sys
import math
import PreTTY
import os
from balls import reload_screen
"""
Code for class based GUI object.
"""


class app(object):
    def __init__(self, parent):
        #Background and foreground colors
        self.bg_c = "black"
        self.fg_c = "white"

        # Percentage of user's screen GUI initially takes up
        self.window_scale = 0.80

        #Ratio between X and Y dimensions
        self.ScreenRatio = 1.0

        #Render and create GUI window
        self.window_setup(parent)

        #Create and render application title/logo
        self.title_setup()

        #Specify GUI hotkeys
        self.hotkey_setup()

        #Initialize text windows (file viewer/graveyard/help)
        self.text_setup()

        #Create and render file canvas
        self.canvas_setup()

        #Initialize and create buttons
        self.button_setup()

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
        PreTTY.command_parse(event.widget.get())
        event.widget.delete(0, tk.END)

    #Toggle left hand display
    def toggle_left(self, event=''):
        if(self.left_bool):
            self.left_txt_frame.pack_forget()
        else:
            self.left_txt_frame.pack(side=tk.LEFT)

        self.left_bool = (self.left_bool + 1) % 2

    # Toggle return to Desktop
    def toggle_Desktop(self, event=''):
        reload_screen(self.desktop, self)




    # Toggle return to Desktop
    def ToggleBack_button(self, event=''):
        reload_screen(os.path.split(self.backhistory)[0], self)


    #Toggle right hand display
    def toggle_right(self, event=''):
        if(self.right_bool):
            self.right_txt_frame.pack_forget()

        else:
            if(self.help_bool):  # If the help window is open, close it and then open the graveyard window
                self.toggle_help()
            self.right_txt_frame.pack(side=tk.RIGHT)

        self.right_bool = (self.right_bool + 1) % 2

    #Toggle help text display
    def toggle_help(self, event=''):
        if(self.help_bool):
            self.help_txt_frame.pack_forget()
        else:
            if(self.right_bool):
                self.toggle_right()
            self.help_txt_frame.pack(side=tk.RIGHT)

        self.help_bool = (self.help_bool + 1) % 2

    #TODO: Optimize this so function does not become too big
    #Toggle between light and dark themes
    def toggle_theme(self, event=''):
        if(self.theme_bool):

            #dark theme
            self.root.config(bg="black")
            self.prompt_frame.config(bg="black")
            self.left_window.config(bg="black", fg="white")
            self.right_window.config(bg="black", fg="white")
            self.canvas.config(bg="black")

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
            self.canvas.config(bg="white")

            #Application title displayed on window
            self.app_name.pack_forget()
            self.app_logo = tk.PhotoImage(file="graphics/logo.gif")
            self.app_logo = self.app_logo.subsample(2, 2)
            self.app_name = tk.Label(
                self.root, image=self.app_logo, bg="white")

            self.app_name.pack(side=tk.TOP)

        self.theme_bool = (self.theme_bool + 1) % 2

    #Creates and renders buttons for GUI
    def button_setup(self):
        #Create button frame and placement
        self.prompt_frame = tk.Frame(self.root, bg=self.bg_c)
        self.prompt_frame.pack(side=tk.BOTTOM)

        #Buttons to hide and show text display
        self.left_display_button = tk.Button(
            self.prompt_frame, text="File View", command=self.toggle_left)
        self.left_display_button.grid(row=0, column=0)

        #Buttons to return to Desktop
        self.Desktop_button = tk.Button(
            self.prompt_frame, text="Desktop", command=self.toggle_Desktop)
        self.Desktop_button.grid(row=3, column=4)

        #Buttons to hide and show text display
        self.Back_button = tk.Button(
            self.prompt_frame, text="Back", command=self.ToggleBack_button)
        self.Back_button.grid(row=2, column=2)


        #Gravestone button to trigger graveyard
        self.gravestone = tk.PhotoImage(file="graphics/Gravestone.gif")
        self.gravestone = self.gravestone.subsample(20, 20)

        self.graveyard_switch = tk.Label(
            self.prompt_frame, image=self.gravestone, bg=self.bg_c, fg=self.fg_c)
        self.graveyard_switch.grid(row=0, column=3)

        self.graveyard_switch.bind("<Button-1>", self.toggle_right)

        #Help window toggle button
        #self.help_button = tk.Button(
        #    self.prompt_frame, text="Help", command=self.toggle_help)
        #self.help_button.grid(row=0, column=4)

        #Light dark theme toggle button
        self.themepic = tk.PhotoImage(file="graphics/theme_button.gif")
        self.themepic = self.themepic.subsample(2, 2)

        self.theme_switch = tk.Label(
            self.prompt_frame, image=self.themepic, bg=self.bg_c, fg=self.fg_c)
        self.theme_switch.grid(row=0, column=1)

        self.theme_switch.bind("<Button-1>", self.toggle_theme)

        #Help window toggle button
        #self.help_button = tk.Button(
        #    self.prompt_frame, text="Help", command=self.toggle_help)
        #self.help_button.grid(row=0, column=4)
        self.helppic = tk.PhotoImage(file="graphics/help_button.gif")
        self.helppic = self.helppic.subsample(19, 19)

        self.help_switch = tk.Label(
            self.prompt_frame, image=self.helppic, bg=self.bg_c, fg=self.fg_c)
        self.help_switch.grid(row=0, column=4)

        self.help_switch.bind("<Button-1>", self.toggle_help)

        #Command prompt--------------------------------------
        #TODO: Add hotkey to set focus easily
        e = tk.Entry(self.prompt_frame, width=25)
        e.focus()
        e.bind('<Return>', self.get)
        e.grid(row=0, column=2)

    #Creates and renders canvas for GUI
    def canvas_setup(self):
        #Canvas frame setup and placement
        self.canvas_frame = tk.Frame(self.root, bg=self.bg_c)
        self.canvas_frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

        #Canvas for file display
        self.canvas = tk.Canvas(self.canvas_frame, width=int(
            self.ScreenSizeX*(0.5)), height=int(self.ScreenSizeY*(0.65)), bg="black")
        self.canvas.configure(scrollregion=(0, 0, 1000, 1000))
        self.canvas.grid(row=0, column=0, sticky='nsew')

        #Canvas scroll bar
        canvasScrollbr = tk.Scrollbar(
            self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        canvasScrollbr.grid(row=0, column=1, sticky='nsew')
        self.canvas.config(yscrollcommand=canvasScrollbr.set)

        #Canvas scroll bar


        canvasScrollbr = tk.Scrollbar(
            self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        canvasScrollbr.grid(row=1, column=0, sticky='nsew')
        self.canvas.config(xscrollcommand=canvasScrollbr.set)

    #Initalizes text windows
    def text_setup(self):
        #Toggle switches
        self.theme_bool = 0
        self.left_bool = 0
        self.right_bool = 0
        self.help_bool = 0

        #Text Frames
        self.left_txt_frame = tk.Frame(self.root, bg=self.bg_c)
        self.right_txt_frame = tk.Frame(self.root, bg=self.bg_c)
        self.help_txt_frame = tk.Frame(self.root, bg=self.bg_c)

        #Left Hand Text Display (File Directory)
        #TODO: Change this to be interactive, clickable
        self.left_window = tk.Text(
            self.left_txt_frame, width=40, height=60, wrap=tk.WORD, bg=self.bg_c, fg=self.fg_c)
        self.left_window.grid(row=0, column=0, sticky='nsew')

        #Left scroll bar
        leftScrollbr = tk.Scrollbar(
            self.left_txt_frame, command=self.left_window.yview)
        leftScrollbr.grid(row=0, column=1, sticky='nsew')
        self.left_window['yscrollcommand'] = leftScrollbr.set

        #Right Hand Text Display (Graveyard)
        self.right_window = tk.Text(
            self.right_txt_frame, width=40, height=60, wrap=tk.WORD, bg=self.bg_c, fg=self.fg_c)
        self.right_window.grid(row=0, column=0, sticky='nsew')

        #Right scroll bar
        rightScrollbr = tk.Scrollbar(
            self.right_txt_frame, command=self.right_window.yview)
        rightScrollbr.grid(row=0, column=1, sticky='nsew')
        self.right_window['yscrollcommand'] = rightScrollbr.set

        #Help Text Window
        self.help_window = tk.Text(
            self.help_txt_frame, width=40, height=60, wrap=tk.WORD, bg=self.bg_c, fg=self.fg_c)
        self.help_window.grid(row=0, column=0, sticky='nsew')

        #Help Window Scroll Bar
        helpScrollbr = tk.Scrollbar(
            self.help_txt_frame, command=self.help_window.yview)
        helpScrollbr.grid(row=0, column=1, sticky='nsew')
        self.help_window['yscrollcommand'] = helpScrollbr.set

    #Specify GUI hotkeys
    def hotkey_setup(self):
        #Hot keys
        self.root.bind_all("<Control-w>", self.quit)
        self.root.bind_all("<Control-f>", self.toggle_left)
        self.root.bind_all("<Control-h>", self.toggle_help)
        self.root.bind_all("<Control-g>", self.toggle_right)

    def title_setup(self):
        #Application title displayed on window
        self.root.title("preTTy")
        self.app_logo = tk.PhotoImage(file="graphics/logo_light.gif")
        self.app_logo = self.app_logo.subsample(2, 2)
        self.app_name = tk.Label(
            self.root, image=self.app_logo, bg=self.bg_c, fg=self.fg_c)

        self.app_name.pack(side=tk.TOP)

    def window_setup(self, parent):
        #Designate root window
        self.root = parent

        #Calculates screen size and centers window position
        # Get screen width and height [pixels]
        self.ScreenSizeX = self.root.winfo_screenwidth()
        self.ScreenSizeY = self.root.winfo_screenheight()

        #Temporary fix for duel monitor set up
        if(self.ScreenSizeX - self.ScreenSizeY > 2000):
            self.ScreenSizeX = self.ScreenSizeX/2

        #Scale gui size to specified % of total screen
        self.ScreenSizeX *= self.window_scale
        self.ScreenSizeY *= self.window_scale

        # Set the screen ratio for width and height
        FrameSizeX = int(self.ScreenSizeX * self.ScreenRatio)
        FrameSizeY = int(self.ScreenSizeY * self.ScreenRatio)

        # Find left and up border of window
        FramePosX = int(math.ceil((self.ScreenSizeX - FrameSizeX)/2))
        FramePosY = int(math.ceil((self.ScreenSizeY - FrameSizeY)/2))
        self.root.geometry("%sx%s+%s+%s" %
                           (FrameSizeX, FrameSizeY, FramePosX, FramePosY))

        self.root.configure(background=self.bg_c)

    #Close app
    def quit(self, event):
        sys.exit(0)
