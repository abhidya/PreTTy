import tkinter as tk
import subprocess

#TODO: Decide whether to use grid or pack approach for labels
class app(object):
    def __init__(self, parent):
        self.root = parent
        self.root.title("preTTY")
        self.root.geometry("800x500")
        self.root.configure(background="black")


        #Application title displayed on window
        self.app_name = tk.Label(self.root, text="preTTY", bg="black", fg="white", font="none 30 bold")
        self.app_name.pack(side=tk.TOP)

        #Box to display current dirctory
        #TODO: Change this to be interactive
        self.output = tk.Text(self.root, width=40, height=60, wrap=tk.WORD, bg="black", fg="white")
        
        #Buttons to hide and show text display
        #TODO: Change to one button that toggles display
        file_toggle = tk.Button(self.root, text="file view", command=self.hide_me);
        file_toggle_show = tk.Button(self.root, text="file view-show", command=self.show_me);

        file_toggle.pack(side=tk.BOTTOM)
        file_toggle_show.pack(side=tk.BOTTOM)

        #Command prompt
        #TODO: Add autofocus when app is first accessed
        #TODO: Add hotkey to set focus easily
        e = tk.Entry(self.root, width=25)
        e.bind('<Return>',self.get)
        e.pack(side=tk.BOTTOM)
        e.focus()

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
        self.output.pack_forget()

    #shows the lefthand text box
    def show_me(self):
        self.output.pack(side=tk.LEFT)


if __name__ == "__main__":
    root = tk.Tk()
    gui = app(root)
    root.mainloop()
