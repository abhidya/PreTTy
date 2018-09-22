import tkinter as tk
import PIL
from PIL import Image, ImageTk

# --- functions ---

def on_click(event=None):
    # `command=` calls function without argument
    # `bind` calls function with one argument
    print("image clicked")

# --- main ---

root = tk.Tk()

# load image and resize it
basewidth = 200
image = Image.open("../gui/images/alpaca.gif")
#photo = ImageTk.PhotoImage(image)
wpercent = (basewidth / float(image.size[0]))
hsize = int((float(image.size[1]) * float(wpercent)))
image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
image.save("resized_image.gif") 
photo = ImageTk.PhotoImage(image)

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

root.geometry("500x300")
root.mainloop()