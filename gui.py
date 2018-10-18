import tkinter as tk
import sys
"""
Code for class based GUI object.
"""

class app(object):
    def __init__(self, parent):
        bg_c = "black"
        fg_c = "white"
        #rows = 0
        #grid_size = 1 

        self.root = parent
        self.root.title("preTTy")

        #TODO: Add flexibility to window size, take into account system constraints
        self.root.geometry("1200x750")
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

        self.prompt_frame.pack(side=tk.BOTTOM)

        #while rows < 50:
        #    self.root.rowconfigure(rows, minsize=grid_size)
        #    self.root.columnconfigure(rows, minsize=grid_size)
        #    rows += 1

        #self.prompt_frame.grid(row=49, column=25)

        #Application title displayed on window
        self.app_logo = tk.PhotoImage(file="graphics/logo_light.gif")
        self.app_logo = self.app_logo.subsample(2, 2)
        self.app_name = tk.Label(
            self.root, image=self.app_logo, bg=bg_c, fg=fg_c)

        self.app_name.pack(side=tk.TOP)
        #self.app_name.grid(row=0, column=25)

        #Box to display current dirctory
        #TODO: Change this to be interactive, clickable
        self.left_window = tk.Text(
            self.root, width=40, height=60, wrap=tk.WORD, bg=bg_c, fg=fg_c)
        self.right_window = tk.Text(
            self.root, width=40, height=60, wrap=tk.WORD, bg=bg_c, fg=fg_c)

        #Buttons to hide and show text display
        #TODO: Add right display button
        self.left_display_button = tk.Button(
            self.prompt_frame, text="file view", command=self.toggle_left)
        self.left_display_button.grid(row=0, column=0)

        #Command prompt
        #TODO: Add hotkey to set focus easily
        e = tk.Entry(self.prompt_frame, width=25)
        e.focus()
        e.bind('<Return>', self.get)
        e.grid(row=1, column=0)

        #Light / Dark theme toggle button
        self.theme_button = tk.Button(
            self.root, text="theme", command=self.theme_toggle)

        self.theme_button.pack(side=tk.BOTTOM)
        #self.theme_button.grid(row=48, column=25)

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
        self.update_text(self.left_window, event.widget.get())
        event.widget.delete(0, tk.END)

    def toggle_left(self, event=''):
        if(self.left_bool):
            self.left_window.pack_forget()
            #self.left_window.grid_forget()
        else:
            #self.left_window.grid(row=24, column=0)
            self.left_window.pack(side=tk.LEFT)

        self.left_bool = (self.left_bool + 1) % 2

    def toggle_right(self, event=''):
        if(self.right_bool):
            self.right_window.pack_forget()
            #self.right_window.grid_forget()
        else:
            #self.right_window.grid(row=24, column=49)
            self.right_window.pack(side=tk.RIGHT)

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
