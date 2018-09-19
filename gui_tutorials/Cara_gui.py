import tkinter as tk
from PIL import Image, ImageTk

# --- functions ---

# --- main ---

root = tk.Tk()

# load image
image = Image.open("../gui/images/apple.gif")
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
b = tk.Button(root, text="Close", command=root.destroy)
b.pack()

#b = tk.Button(root)
#photo = tk.PhotoImage(file="BadHombre.png")
#b.config(image=photo,width="100",height="100")
#b.pack(side=LEFT)

root.geometry("1000x725")
root.mainloop()