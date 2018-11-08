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
        window_scale = 0.75
        

        #Designate root window
        self.root = parent
        self.root.title("preTTy")

        #Calculates screen size and centers window position
        # Get screen width [pixels]
        ScreenSizeX = self.root.winfo_screenwidth()
        # Get screen height [pixels]
        ScreenSizeY = self.root.winfo_screenheight()

        #Temporary fix for duel monitor set up
        if(ScreenSizeX - ScreenSizeY > 2000):
            ScreenSizeX = ScreenSizeX/2

        #Scale gui size to specified % of total screen
        ScreenSizeX *= window_scale
        ScreenSizeY *= window_scale

        # Set the screen ratio for width and height
        ScreenRatio = 1.0
        FrameSizeX = int(ScreenSizeX * ScreenRatio)
        FrameSizeY = int(ScreenSizeY * ScreenRatio)

        # Find left and up border of window
        FramePosX = int(math.ceil((ScreenSizeX - FrameSizeX)/2))
        FramePosY = int(math.ceil((ScreenSizeY - FrameSizeY)/2))
        self.root.geometry("%sx%s+%s+%s" %(FrameSizeX, FrameSizeY, FramePosX, FramePosY))

        #self.root.geometry("1200x750")
        self.root.configure(background=bg_c)

        #Hot keys
        self.root.bind_all("<Control-w>", self.quit)
        self.root.bind_all("<Control-f>", self.toggle_left)
        self.root.bind_all("<Control-h>", self.toggle_help)
        self.root.bind_all("<Control-g>", self.toggle_right)

        #Toggle switches
        self.theme_bool = 0
        self.left_bool = 0
        self.right_bool = 0
        self.help_bool = 0

        #Frame to hold prompt and left display toggle
        self.prompt_frame = tk.Frame(self.root, bg=bg_c)

        #Text Frames
        self.left_txt_frame = tk.Frame(self.root, bg=bg_c)
        self.right_txt_frame = tk.Frame(self.root, bg=bg_c)

        self.canvas_frame = tk.Frame(self.root, bg=bg_c)

        self.prompt_frame.pack(side=tk.BOTTOM)

        #Application title displayed on window
        self.app_logo = tk.PhotoImage(file="graphics/logo_light.gif")
        self.app_logo = self.app_logo.subsample(2, 2)
        self.app_name = tk.Label(self.root, image=self.app_logo, bg=bg_c, fg=fg_c)

        self.app_name.pack(side=tk.TOP)

        #Left Hand Text Display (File Directory)
        #TODO: Change this to be interactive, clickable
        self.left_window = tk.Text(self.left_txt_frame, width=40, height=60, wrap=tk.WORD, bg=bg_c, fg=fg_c)
        self.left_window.grid(row=0, column=0, sticky='nsew')

        #Left scroll bar
        leftScrollbr = tk.Scrollbar(self.left_txt_frame, command=self.left_window.yview)
        leftScrollbr.grid(row=0, column=1, sticky='nsew')
        self.left_window['yscrollcommand'] = leftScrollbr.set

        #Right Hand Text Display (Graveyard)
        self.right_window = tk.Text(self.right_txt_frame, width=40, height=60, wrap=tk.WORD, bg=bg_c, fg=fg_c)
        self.right_window.grid(row=0, column=0, sticky='nsew')

        #Right scroll bar
        rightScrollbr = tk.Scrollbar(self.right_txt_frame, command=self.right_window.yview)
        rightScrollbr.grid(row=0, column=1, sticky='nsew')
        self.right_window['yscrollcommand'] = rightScrollbr.set

        self.canvas = tk.Canvas(self.canvas_frame, width=1000, height=750, bg="black")

        #self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self.canvas.configure(scrollregion = (0,0,1000,1000))

        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.canvas_frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

        #Canvas scroll bar
        canvasScrollbr = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        canvasScrollbr.grid(row=0, column=1, sticky='nsew')
        self.canvas.config(yscrollcommand=canvasScrollbr.set)

        #Window for help
        self.help_window = tk.Text(self.root, width=40, height=60, wrap=tk.WORD, bg=bg_c, fg=fg_c)

        #Buttons to hide and show text display
        self.left_display_button = tk.Button(self.prompt_frame, text="File View", command=self.toggle_left)
        self.left_display_button.grid(row=0, column=0)

        self.gravestone = tk.PhotoImage(file="graphics/Gravestone.gif")
        self.gravestone = self.gravestone.subsample(20, 20)
        self.graveyard_switch = tk.Label(self.prompt_frame, image=self.gravestone, bg=bg_c,fg=fg_c)
        self.graveyard_switch.grid(row=0,column=3)

        self.graveyard_switch.bind("<Button-1>", self.toggle_right)
        
        #Help window toggle button
        self.help_button = tk.Button(self.prompt_frame, text="Help", command=self.toggle_help)
        self.help_button.grid(row = 0, column = 4)
     
        #load light and dark theme toggle button
        self.themepng = tk.PhotoImage(file="graphics/theme_button.gif")
        self.themepng = self.themepng.subsample(2, 2)

        #Command prompt
        #TODO: Add hotkey to set focus easily
        e = tk.Entry(self.prompt_frame, width=25)
        e.focus()
        e.bind('<Return>', self.get)
        e.grid(row=0, column=2)

        #Light / Dark theme toggle button
        self.theme_button = tk.Button(
            self.prompt_frame, text="Theme", command=self.theme_toggle)
        self.theme_button.grid(row = 0, column = 1)

        #Help window toggle button
        self.help_button = tk.Button(self.prompt_frame, text="Help", command=self.toggle_help)
        self.help_button.grid(row = 0, column = 4)

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
            #self.grave_stone = tk.Label(self.root, image=self.gravestonepng,bg="black", fg="white")

            #self.grave_stone.pack(side=tk.RIGHT)

            #self.grave_stone.bind("<Button-1>", self.toggle_right)

        else:
            if(self.help_bool):                   #If the help window is open, close it and then open the graveyard window
                self.toggle_help()
            self.right_txt_frame.pack(side=tk.RIGHT)
            #self.grave_stone.destroy()

        self.right_bool = (self.right_bool + 1) % 2

    def toggle_help(self, event=''):
        if(self.help_bool):
            self.help_window.pack_forget()
        else:
            if(self.right_bool):
                self.toggle_right()
            self.help_window.pack(side=tk.RIGHT)

        self.help_bool = (self.help_bool + 1) % 2

    #TODO: Optimize this so function does not become too big
    #Toggle between light and dark themes
    def theme_toggle(self):
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


    #Close app
    def quit(self, event):
        sys.exit(0)
