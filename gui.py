import tkinter as tk
import sys
import math
import PreTTY
import os
import Graveyard
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
        self.button_setup(
            0, self.bg_c, "graphics/GIF_files/help_button_dark.gif")

        self.graveyard_setup()

        self.k = 8
        self.layouts = [1, 2, 3, 4, 8]

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
        PreTTY.balls.reload_screen(self.desktoppath, self)

    # Toggle return to Desktop

    def toggle_Layout_button(self, event=''):
        self.k = self.layouts[0]
        self.layouts.append(self.layouts.pop(0))
        PreTTY.balls.reload_screen(self.backhistory, self)

    # Toggle return to Desktop

    def ToggleBack_button(self, event=''):
        PreTTY.balls.reload_screen(os.path.split(self.backhistory)[0], self)

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

    #Retrieve current parameters for graveyard (10 Months, 15 Days...)
    def get_graveyard_param(self):
        Graveyard.initGraveyard(
            int(self.graveyard_entry.get()), self.graveyard_var.get())

    #Function to setup and create graveyard frame for dropdown settings
    def graveyard_setup(self):
        #Frame to hold all template components
        self.graveyard_setting_frame = tk.Frame(
            self.right_txt_frame, bg=self.bg_c)

        #Create dropdown element and grid
        self.graveyard_var = tk.StringVar()
        options = ['Day(s)', 'Week(s)', 'Month(s)', 'Year(s)']
        self.graveyard_var.set('Month(s)')
        self.graveyard_dropdown = tk.OptionMenu(
            self.graveyard_setting_frame, self.graveyard_var, *options)
        self.graveyard_dropdown.grid(row=1, column=1, sticky=tk.W)

        #Create text entry element and grid
        self.graveyard_entry = tk.Entry(self.graveyard_setting_frame)
        self.graveyard_entry.delete(0, tk.END)
        self.graveyard_entry.insert(0, 6)
        self.graveyard_entry.grid(row=1, column=0, sticky=tk.W)

        #Create label and grid
        self.graveyard_label = tk.Label(self.graveyard_setting_frame, text="Time before files await burial.").grid(
            row=0, column=0, columnspan=2, sticky=tk.W)

        #Create submit button and grid
        self.graveyard_commit = tk.Button(
            self.graveyard_setting_frame, text="Ok", command=self.get_graveyard_param)
        self.graveyard_commit.grid(row=1, column=2, sticky=tk.W)
        
        #Grid finished frame in master frame
        self.graveyard_setting_frame.grid(row=1, column=0)

    #Creates and renders buttons for GUI
    def button_setup(self, x, color, file_name):
        if(x == 0):
            #Create button frame and placement
            self.prompt_frame = tk.Frame(self.root, bg=self.bg_c)
            self.prompt_frame.pack(side=tk.BOTTOM)
            x = 1

        #Buttons to hide and show text display
        self.file_view_button = tk.PhotoImage(
            file="graphics/GIF_files/file_viewing_button.gif")
        self.file_view_button = self.file_view_button.subsample(20, 20)

        self.file_view = tk.Label(
            self.prompt_frame, image=self.file_view_button, bg=color, fg=self.fg_c)
        self.file_view.grid(row=0, column=0, padx=10)

        self.file_view.bind("<Button-1>", self.toggle_left)

        # Buttons to return to Desktop
        self.desktop_button = tk.PhotoImage(
            file="graphics/GIF_files/desktop_button.gif")
        self.desktop_button = self.desktop_button.subsample(20, 20)

        self.desktop = tk.Label(
            self.prompt_frame, image=self.desktop_button, bg=color, fg=self.fg_c)
        self.desktop.grid(row=0, column=1, padx=10)

        self.desktop.bind("<Button-1>", self.toggle_Desktop)

        # Buttons to cycle through layout
        self.layout_button = tk.PhotoImage(
            file="graphics/GIF_files/theme_change_button.gif")
        self.layout_button = self.layout_button.subsample(20, 20)

        self.layout = tk.Label(
            self.prompt_frame, image=self.layout_button, bg=color, fg=self.fg_c)
        self.layout.grid(row=0, column=2, padx=10)

        self.layout.bind("<Button-1>", self.toggle_Layout_button)

        self.back_button = tk.PhotoImage(
            file="graphics/GIF_files/back_button.gif")
        self.back_button = self.back_button.subsample(20, 20)

        self.back = tk.Label(
            self.prompt_frame, image=self.back_button, bg=color, fg=self.fg_c)
        self.back.grid(row=0, column=3, padx=10)

        self.back.bind("<Button-1>", self.ToggleBack_button)

        #Gravestone button to trigger graveyard
        self.gravestone = tk.PhotoImage(
            file="graphics/GIF_files/Gravestone.gif")
        self.gravestone = self.gravestone.subsample(20, 20)

        self.graveyard_switch = tk.Label(
            self.prompt_frame, image=self.gravestone, bg=color, fg=self.fg_c)
        self.graveyard_switch.grid(row=0, column=4, padx=10)

        self.graveyard_switch.bind("<Button-1>", self.toggle_right)

        #Light dark theme toggle button
        self.themepic = tk.PhotoImage(
            file="graphics/GIF_files/theme_button.gif")
        self.themepic = self.themepic.subsample(2, 2)

        self.theme_switch = tk.Label(
            self.prompt_frame, image=self.themepic, bg=color, fg=self.fg_c)
        self.theme_switch.grid(row=0, column=5, padx=10)

        self.theme_switch.bind("<Button-1>", self.toggle_theme)

        #Help window toggle button
        self.helppic = tk.PhotoImage(file=file_name)
        self.helppic = self.helppic.subsample(19, 19)

        self.help_switch = tk.Label(
            self.prompt_frame, image=self.helppic, bg=color, fg=self.fg_c)
        self.help_switch.grid(row=0, column=6, padx=10)

        self.help_switch.bind("<Button-1>", self.toggle_help)

    #Toggle between light and dark themes
    def toggle_theme(self, event=''):
        logo_gif = ""
        help_gif = ""
        self.app_name.pack_forget()

        #dark theme
        if(self.theme_bool):
            self.bg_c = "black"
            self.fg_c = "white"
            help_gif = "_dark.gif"
            logo_gif = "_light.gif"

        #white theme
        else:
            self.bg_c = "white"
            self.fg_c = "black"
            help_gif = "_light.gif"
            logo_gif = "_dark.gif"

        #change background of buttons
        self.button_setup(
            1, self.bg_c, "graphics/GIF_files/help_button"+help_gif)

        #Application title displayed on window
        self.app_logo = tk.PhotoImage(file="graphics/GIF_files/logo"+logo_gif)
        self.app_logo = self.app_logo.subsample(2, 2)
        self.app_name = tk.Label(
            self.root, image=self.app_logo, bg=self.bg_c)
        self.app_name.pack(side=tk.TOP)

        #Set new colors of elements
        self.root.config(bg=self.bg_c)
        self.prompt_frame.config(bg=self.bg_c)
        self.left_window.config(bg=self.bg_c, fg=self.fg_c)
        self.right_window.config(bg=self.bg_c, fg=self.fg_c)
        self.help_window.config(bg=self.bg_c, fg=self.fg_c)
        self.graveyard_setting_frame.config(bg=self.bg_c)
        self.right_txt_frame.config(bg=self.bg_c)
        self.canvas.config(bg=self.bg_c)
        self.canvas_frame.config(bg=self.bg_c)
        self.textcolor = self.fg_c

        PreTTY.balls.reload_screen(self.backhistory, self)

        self.theme_bool = (self.theme_bool + 1) % 2

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
        #self.left_window = tk.Text(
        #    self.left_txt_frame, width=40, height=60, wrap=tk.WORD, bg=self.bg_c, fg=self.fg_c)
        self.left_window = tk.Text(
            self.left_txt_frame, width=int(self.ScreenSizeX*.02), height=int(self.ScreenSizeY*.065), wrap=tk.WORD, bg=self.bg_c, fg=self.fg_c)
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
        self.app_logo = tk.PhotoImage(file="graphics/GIF_files/logo_light.gif")
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
