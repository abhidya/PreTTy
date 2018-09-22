import tkinter as tk
import subprocess


#TODO: Change to class based implementation
#TODO: Decide whether to use grid or pack approach for labels

#command is a string retrieved from text box
def updateWindow(command=''):
    output.config(state=tk.NORMAL)
    output.delete(0.0,tk.END)
    p = subprocess.Popen(["ls", "-al"], stdout=subprocess.PIPE)
    current_dir = p.communicate()[0]
    output.insert(tk.END, current_dir)
    output.config(state=tk.DISABLED)


def get(event):
    updateWindow(event.widget.get())

#hides the lefthand text box
def hide_me():
    output.pack_forget()

#shows the lefthand text box
def show_me():
    output.pack(side=tk.LEFT)

root = tk.Tk()
root.geometry("800x500")
root.title("preTTY")
root.configure(background="black")

#Application title displayed on window
app_name = tk.Label(root, text="preTTY", bg="black", fg="white", font="none 30 bold")
app_name.pack(side=tk.TOP)

#Box to display current dirctory
#TODO: Change this to be interactive
output = tk.Text(root, width=40, height=60, wrap=tk.WORD, bg="black", fg="white")

#Buttons to hide and show text display
#TODO: Change to one button that toggles display
file_toggle = tk.Button(root, text="file view", command=hide_me);
file_toggle_show = tk.Button(root, text="file view-show", command=show_me);

file_toggle.pack(side=tk.BOTTOM)
file_toggle_show.pack(side=tk.BOTTOM)

#Command prompt
#TODO: Add autofocus when app is first accessed
#TODO: Add hotkey to set focus easily
e = tk.Entry(root, width=25)
e.bind('<Return>',get)
e.pack(side=tk.BOTTOM)

updateWindow()
root.mainloop()
