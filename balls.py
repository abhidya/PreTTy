import os
import platform
import SizeScaler
import random
import tkinter as tk
import icongetter
from PIL import Image, ImageTk
import PreTTY
import balls
import Points_bcknd as points


def open_file(path, center_display, root, gui):
    def reload_screen(path, center_display, root, gui):
        center_display.delete("all")

        path = path + "/"

        initial_dir = PreTTY.setup(path)
        # tempArray[0] is normal file percentiles and tempArray[1] is graveyard files
        tempArray = SizeScaler.get_percentiles()
        percentiles = tempArray[0]
        graveyardFiles = tempArray[1]

        # Uncomment this in order to create a dictionary of all files not in the graveyard
        nonGraveyardFiles = {}
        for i, j in percentiles.items():
            if i in graveyardFiles:
                continue

            for item in initial_dir:
                # print(i, item[0])
                if i == item[0]:
                    nonGraveyardFiles[i] = j

        # Render center canvas
        center_display = balls.create_balls(root)
        center_display.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Print current directory to left hand display
        if len(initial_dir) == 0:  # If all files belong in the graveyard
            gui.append_text(gui.left_window, "All files in graveyard!")
        for k, v in initial_dir:
            if k in graveyardFiles:  # If a file is in the graveyard, don't print it to the left window
                continue
            gui.append_text(gui.left_window, str(os.path.basename(k)) + "\n")

        # Render current dir files to canvas
        balls.update_ball_gui(center_display, nonGraveyardFiles, root, gui)

    if os.path.isdir(path):
        reload_screen(path, center_display, root, gui)
        return

    usersOS = platform.system()

    if (usersOS == "Linux"):
        os.system("xdg-open " + path)
        dir_path = os.path.dirname(os.path.realpath(path))
        reload_screen(dir_path, center_display, root, gui)
        return

    elif (usersOS == "Windows"):
        os.system("start " + path)
        dir_path = os.path.dirname(os.path.realpath(path))
        reload_screen(dir_path, center_display, root, gui)
        return

    elif (usersOS == "Darwin"):
        dir_path = os.path.dirname(os.path.realpath(path))
        reload_screen(dir_path, center_display, root, gui)
        os.system("open " + path)
        return

    else:
        try:  # linux
            os.system("xdg-open " + path)
            dir_path = os.path.dirname(os.path.realpath(path))
            reload_screen(dir_path, center_display, root, gui)
            return
        except:
            pass
        try:  # Windows
            os.system("start " + path)
            dir_path = os.path.dirname(os.path.realpath(path))
            reload_screen(dir_path, center_display, root, gui)
            return
        except:
            pass
        try:  # MacOS
            os.system("open " + path)
            dir_path = os.path.dirname(os.path.realpath(path))

            reload_screen(dir_path, center_display, root, gui)
            return
        except:
            pass


def onClick(fileName, center_display, root, gui):
    open_file(fileName, center_display, root, gui)
    points.addPoint(fileName)


# takes a dictionary containing numbers 1-n for n percentiles and scales the size of ovals
def create_balls(parent):
    canvas = tk.Canvas(parent, width=1000, height=750, bg="black")
    return canvas


def update_ball_gui(canvas, percentiles, root, gui):
    width = 0
    height = 10
    min_radius = 25
    text_limit = 15

    s = [(k, percentiles[k]) for k in sorted(percentiles, key=percentiles.get)]

    for file, rank in s:
        path_lists = file.split('/')
        path_lists.reverse()
        file2 = path_lists[0]

        # Shorten file name if too long to display
        if len(file2) > text_limit:
            file2 = file2[0:8] + "..."

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

        img = Image.open(icongetter.extension(file))

        img = img.resize((rank * min_radius, rank * min_radius), Image.ANTIALIAS)
        photoImg = ImageTk.PhotoImage(img)

        label = tk.Label(image=photoImg)
        label.image = photoImg
        label.pack

        oval = canvas.create_image((x0, y0 + rank * min_radius), image=photoImg)

        colors = ["blue", "orange", "red", "green"]
        canvas.tag_bind(oval, "<Button-1>", lambda event, arg=file: onClick(
            arg, canvas, root, gui))  # Calls onClick and passes it the file name for backend handling
        canvas.create_text((x0, y0), text=file2, fill=random.choice(colors))

        if 70 <= width + 5 * min_radius <= 930:
            width = width + 5 * min_radius
        else:
            width = 100
            height = height + 5 * min_radius + 30
