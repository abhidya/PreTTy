import tkinter as tk
import PIL
from PIL import Image, ImageTk

# --- functions ---
#<<<<<<< HEAD

def on_click(event=None):
    # `command=` calls function without argument
    # `bind` calls function with one argument
    print("image clicked")


# --- main ---

root = tk.Tk()

# load image and resize it
basewidth = 200
photo = Image.open("../gui/images/alpaca.gif")
wpercent = (basewidth / float(photo.size[0]))
hsize = int((float(photo.size[1]) * float(wpercent)))
photo = photo.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
photo.save("resized_image.gif") 
photo = ImageTk.PhotoImage(photo)

# label with image
l = tk.Label(root, image=photo)
l.pack()

# bind click event to image
l.bind('<Button-1>', on_click)

# button with image binded to the same function 
b = tk.Button(root, image=photo, command=on_click)
b.pack()

# button with text closing window
b = tk.Button(root, text="Close", fg="red", activeforeground="blue", background="cyan", command=root.destroy)
b.pack()
#bg="#ff340a"

#b = tk.Button(root)
#photo = tk.PhotoImage(file="BadHombre.png")
#b.config(image=photo,width="100",height="100")
#b.pack(side=LEFT)

root.geometry("1000x725")
root.mainloop()