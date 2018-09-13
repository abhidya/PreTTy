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

root = tk.Tk()

root.title("preTTY")
root.configure(background="black")

app_name = tk.Label(root, text="preTTY", bg="black", fg="white", font="none 12 bold")
app_name.pack(side=tk.TOP)

output = tk.Text(root, width=75, height=6, wrap=tk.WORD, background="white")
output.pack(side=tk.BOTTOM)

e = tk.Entry(root, width=25)
e.bind('<Return>',get)
e.pack(side=tk.BOTTOM)

updateWindow()
root.mainloop()
