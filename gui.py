import tkinter as tk
import sys
class app(object):
    def __init__(self, parent):
        bg_c = "black"
        fg_c = "white"
        self.root = parent
        self.root.title("preTTY")
        self.root.geometry("800x500")
        self.root.configure(background=bg_c)
        self.root.bind_all("<Control-q>", self.quit)

        self.prompt_frame = tk.Frame(self.root, bg=bg_c)
        self.prompt_frame.pack(side=tk.BOTTOM)

        #Application title displayed on window
        self.app_name = tk.Label(self.root, text="preTTY", bg=bg_c, fg=fg_c, font="none 30 bold")
        self.app_name.pack(side=tk.TOP)

        #Box to display current dirctory
        #TODO: Change this to be interactive, clickable
        self.output = tk.Text(self.root, width=40, height=60, wrap=tk.WORD, bg=bg_c, fg=fg_c)
        
        #Buttons to hide and show text display
        self.output_hide_button = tk.Button(self.prompt_frame, text="file view", command=self.hide_me);
        self.output_display_button = tk.Button(self.prompt_frame, text="file view", command=self.show_me);
        self.output_display_button.grid(row=0, column=0)

        #Command prompt
        #TODO: Add hotkey to set focus easily
        e = tk.Entry(self.prompt_frame, width=25)
        e.focus()
        e.bind('<Return>',self.get)
        #e.bind('<Control-f>', e.focus) <- Currently not working
        e.grid(row=1, column=0)

        #Light-Dark Button
        self.light_b = tk.Button(self.root, text="light", command=self.light)
        self.light_b.pack(side=tk.RIGHT)


    #Replace contents of text window with data
    def update_text(self, window, data):
        window.config(state=tk.NORMAL)
        window.delete(0.0,tk.END)
        window.insert(tk.END, data)
        window.config(state=tk.DISABLED)

    #Clear contents of text window
    def clear_text(self, window):
        window.delete(0.0,tk.END)

    #Append given data to current data in text window
    def append_text(self, window, data):
        window.config(state=tk.NORMAL)
        window.insert(tk.END, data)
        window.config(state=tk.DISABLED)

    #pulls text from given text widget
    def get(self, event):
        self.update_text(self.output,event.widget.get())
        event.widget.delete(0, tk.END)

    #hides the lefthand text box
    def hide_me(self):
        self.output.pack_forget()
        self.output_hide_button.grid_remove()
        self.output_display_button.grid(row=0,column=0)

    #shows the lefthand text box
    def show_me(self):
        self.output.pack(side=tk.LEFT)
        self.output_display_button.grid_remove()
        self.output_hide_button.grid(row=0,column=0)

    def light(self):
        self.root.config(bg="white")
        self.app_name.config(bg="white", fg="black")
        self.prompt_frame.config(bg="white")
        self.output.config(bg="white",fg="black")

    #Close app
    def quit(self, event):
        sys.exit(0)

