import os
import platform
import tkinter as tk
import icongetter
import Points_bcknd as points


def open_file(path):
    usersOS = platform.system()

    if (usersOS == "Linux"):
        os.system("xdg-open " + path)
        return

    elif (usersOS == "Windows"):
        if os.path.isdir(path):
            os.system("start " + path + "/")
            return
        os.system("start " + path)
        return

    elif (usersOS == "Darwin"):
        os.system("open " + path)
        return

    else:
        try:  # linux
            os.system("xdg-open " + path)
            return
        except:
            pass
        try:  # Windows
            os.system("start " + path)
            return
        except:
            pass
        try:  # MacOS
            os.system("open " + path)
            return
        except:
            pass


def onClick(fileName):
    points.addPoint(fileName)
    open_file(fileName)

#takes a dictionary containing numbers 1-n for n percentiles and scales the size of ovals
#
def ball_gui(percentiles):
    app = tk.Tk()
    canvas = tk.Canvas(app, width=1000, height=1000, bg="gray")
    canvas.pack()

    width = 0
    height = 10
    min_radius = 25

    for file in percentiles:
        path_lists = file.split('/')
        path_lists.reverse()
        file2 = path_lists[0]
        if percentiles[file] == 1:
            x0 = width + 51
            y0 = height + 51
        elif percentiles[file] == 2:
            x0 = width + 38
            y0 = height + 38
        elif percentiles[file] == 3:
            x0 = width + 26
            y0 = height + 26
        elif percentiles[file] == 4:
            x0 = width + 13
            y0 = height + 13
        elif percentiles[file] == 5:
            x0 = width
            y0 = height

        oval = canvas.create_oval(x0, y0, x0 + percentiles[file] * min_radius, y0 + percentiles[file] * min_radius,
                                  tag=file, fill="white")

        canvas.tag_bind(oval, "<Button-1>", lambda event, arg=file: onClick(
            arg))  # Calls onClick and passes it the file name for backend handling
        name_box = tk.Label(app, text=file2)
        name_box.place(x=width + 40, y=height + 127)
        if width + 5 * min_radius <= 1000:
            width = width + 5 * min_radius
        else:
            width = 0
            height = height + 5 * min_radius + 30
    app.mainloop()
