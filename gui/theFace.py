import tkinter as tk
import sys
import subprocess

#TODO: Decide whether to use grid or pack approach for labels (Use grid for detail work, pack for general)
#TODO: Combine command prompt and output window toggle button into one frame
#TODO: Fix window resizing issue when widget is toggled
class app(object):
    def __init__(self, parent):
        self.root = parent
        self.root.title("preTTY")
#        self.root.geometry("800x500")
        self.root.configure(background="black")
        self.root.bind_all("<Control-q>", self.quit)


        #Application title displayed on window
        self.app_name = tk.Label(self.root, text="preTTY", bg="black", fg="white", font="none 30 bold")
        #self.app_name.pack(side=tk.TOP)
        self.app_name.grid(row=0, column=2)

        #Box to display current dirctory
        #TODO: Change this to be interactive
        self.output = tk.Text(self.root, width=40, height=60, wrap=tk.WORD, bg="black", fg="white")
        
        #Buttons to hide and show text display
        #TODO: Change to one button that toggles display
        self.output_hide_button = tk.Button(self.root, text="file view", command=self.hide_me);
        self.output_display_button = tk.Button(self.root, text="file view-show", command=self.show_me);

        #Command prompt
        #TODO: Add hotkey to set focus easily
        e = tk.Entry(self.root, width=25)
        e.bind('<Return>',self.get)
        #e.pack(side=tk.BOTTOM)
        e.grid(row=3, column=2)
        e.focus()

        #self.output_display_button.pack(side=tk.BOTTOM)
        self.output_display_button.grid(row=2, column=2)
        self.updateWindow()

    #command is a string retrieved from text box
    def updateWindow(self, command=''):
        self.output.config(state=tk.NORMAL)
        self.output.delete(0.0,tk.END)
        p = subprocess.Popen(["ls", "-al"], stdout=subprocess.PIPE)
        current_dir = p.communicate()[0]
        self.output.insert(tk.END, current_dir)
        self.output.config(state=tk.DISABLED)


    def get(self, event):
        self.updateWindow(event.widget.get())

    #hides the lefthand text box
    def hide_me(self):
        pass
        #self.output.pack_forget()
        self.output.grid_forget()
       # self.output_hide_button.pack_forget()
        self.output_hide_button.grid_forget()
       # self.output_display_button.pack(side=tk.BOTTOM)
        self.output_display_button.grid(row=2,column=2)

    #shows the lefthand text box
    def show_me(self):
        #self.output.pack(side=tk.LEFT)
        self.output.grid(row=1, column=0)
        #self.output_display_button.pack_forget()
        self.output_display_button.grid_forget()
        #self.output_hide_button.pack(side=tk.BOTTOM)
        self.output_hide_button.grid(row=2,column=2)

    #Close app
    def quit(self, event):
        sys.exit(0)


if __name__ == "__main__":
    root = tk.Tk()
    gui = app(root)
    root.mainloop()
