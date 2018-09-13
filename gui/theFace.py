import tkinter as tk
import subprocess

#command is a string retrieved from text box
def updateWindow(command=''):
    output.delete(0.0,tk.END)
    p = subprocess.Popen(["ls", "-al"], stdout=subprocess.PIPE)
    current_dir = p.communicate()[0]
    output.insert(tk.END, current_dir)


def get(event):
    updateWindow(event.widget.get())

def hide_me():
    output.pack_forget()
def show_me():
    output.pack(side=tk.LEFT)

root = tk.Tk()

root.title("preTTY")
root.configure(background="black")

app_name = tk.Label(root, text="preTTY", bg="black", fg="white", font="none 12 bold")
app_name.pack(side=tk.TOP)

output = tk.Text(root, width=40, height=60, wrap=tk.WORD, bg="black", fg="white")
#output.pack(side=tk.LEFT)

file_toggle = tk.Button(root, text="file view", command=hide_me);
file_toggle_show = tk.Button(root, text="file view-show", command=show_me);

file_toggle.pack(side=tk.LEFT)
file_toggle_show.pack(side=tk.LEFT)

e = tk.Entry(root, width=25)
e.bind('<Return>',get)
e.pack(side=tk.BOTTOM)

updateWindow()
root.mainloop()
