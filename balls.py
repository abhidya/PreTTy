import os
import platform
import SizeScaler
import random
import math
import tkinter as tk
import icongetter
from PIL import Image, ImageTk
import PreTTY
import balls
import Points_bcknd as points


def reload_screen(path, gui):
    gui.canvas.delete("all")
    gui.update_text(gui.left_window, "")
    gui.update_text(gui.right_window, "")

    gui.backhistory = path
    path = path + "/"
    path = path.replace('\\', '/')
    path = path.replace('//', '/')
    if points.checkPickle(path) == 0:
        points.initPickle(path)
    # tempArray[0] is normal file percentiles and tempArray[1] is graveyard files
    tempArray = SizeScaler.get_percentiles(path)
    del tempArray[0][path]
    percentiles = tempArray[0]
    graveyardFiles = tempArray[1]

    nonGraveyardFiles = {}
    for i, j in percentiles.items():
        if i in graveyardFiles:
            continue
        nonGraveyardFiles[i] = j

    # Render center canvas
    # gui.canvas = balls.create_balls(gui.root)
    # gui.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    #
    # Print current directory to left hand display
    if len(nonGraveyardFiles) == 0:  # If all files belong in the graveyard
        gui.append_text(gui.left_window, "All files in graveyard!")
    else:
        for k in nonGraveyardFiles:
            if k in graveyardFiles:  # If a file is in the graveyard, don't print it to the left window
                continue
            gui.append_text(gui.left_window, str(os.path.basename(k)) + "\n")
    if len(graveyardFiles) == 0:
        gui.append_text(gui.right_window, "No files in graveyard!")
    else:
        for k in graveyardFiles:
            gui.append_text(gui.right_window, str(os.path.basename(k)) + "\n")

    # Render current dir files to canvas
    balls.update_ball_gui(gui.canvas, nonGraveyardFiles, gui.root, gui)


def open_file(path, gui):
    if os.path.isdir(path):
        reload_screen(path, gui)
        return

    usersOS = platform.system()

    if (usersOS == "Linux"):
        os.system("xdg-open " + path)
        dir_path = os.path.dirname(os.path.realpath(path))
        reload_screen(dir_path, gui)
        return

    elif (usersOS == "Windows"):
        os.system("start " + path)
        dir_path = os.path.dirname(path)
        reload_screen(dir_path, gui)
        return

    elif (usersOS == "Darwin"):
        dir_path = os.path.dirname(os.path.realpath(path))
        reload_screen(dir_path, gui)
        os.system("open " + path)
        return

    else:
        try:  # linux
            os.system("xdg-open " + path)
            dir_path = os.path.dirname(os.path.realpath(path))
            reload_screen(dir_path, gui)
            return
        except:
            pass
        try:  # Windows
            os.system("start " + path)
            dir_path = os.path.dirname(os.path.realpath(path))
            reload_screen(dir_path, gui)
            return
        except:
            pass
        try:  # MacOS
            os.system("open " + path)
            dir_path = os.path.dirname(os.path.realpath(path))

            reload_screen(dir_path, gui)
            return
        except:
            pass


def onClick(fileName, gui):
    points.addPoint(fileName)
    open_file(fileName, gui)


# takes a dictionary containing numbers 1-n for n percentiles and scales the size of ovals
def create_balls(parent):
    canvas = tk.Canvas(parent, width=1000, height=650, bg="black")
    return canvas


def update_ball_gui(canvas, percentiles, root, gui):
    width = 0
    height = 10
    min_radius = 10
    text_limit = 15
    prevx = 0
    prevy = 0
    s = [(k, percentiles[k]) for k in sorted(percentiles, key=percentiles.get)]
    n = 0
    if gui.k == 66:
        k = random.choice([1, 2, 3, 4, 8])
    else:
        k = gui.k
    # k = random.randint(1,3)

    # k = 8

    for file, rank in s:
        path_lists = file.split('/')
        path_lists.reverse()
        file2 = path_lists[0]

        # Shorten file name if too long to display
        if len(file2) > text_limit:
            file2 = file2[0:6] + "..."

        if rank == 1:
            x0 = width + 51
            y0 = height + 51
        elif rank == 2:
            x0 = width + 38
            y0 = height + 38
        elif rank == 3:
            x0 = width + 26
            y0 = height + 26
        elif rank == 4:
            x0 = width + 13
            y0 = height + 13
        elif rank == 5:
            x0 = width
            y0 = height

        global photoImg

        img = icongetter.extension(file)
        # print(img,file )
        if img is None:
            continue
        img = img.resize((rank * min_radius * 2, rank * min_radius * 2), Image.ANTIALIAS)
        photoImg = ImageTk.PhotoImage(img)

        label = tk.Label(image=photoImg)
        label.image = photoImg
        label.pack

        while True:
            t = n / k * math.pi
            x = (10 * t) * math.cos(t) + 1000 / 2.3
            y = (10 * t) * math.sin(t) + 1000 / 2.5
            n = n + 1
            if math.sqrt((prevx - x) ** 2 + (prevy - y) ** 2) / (math.pi * (rank + 1)/2) >= min_radius * math.sqrt(2):
                prevx = x
                prevy = y
                break
            # prevx = x
            # prevy = y

        oval = canvas.create_image((x, y - min_radius * math.sqrt(2)), image=photoImg)

        color = gui.textcolor
        if gui.textcolor == "skittles":
            colors = ["blue", "orange", "red", "green"]
            color = random.choice(colors)

        canvas.tag_bind(oval, "<Button-1>", lambda event, arg=file: onClick(
            arg, gui))  # Calls onClick and passes it the file name for backend handling
        canvas.create_text((x, y + 30), text=file2, fill=color)

        if 70 <= width + 5 * min_radius <= 930:
            width = width + 5 * min_radius
        else:
            width = 100
            height = height + 5 * min_radius + 30
