import tkinter as tk

#app = tk.Tk()

root = tk.Tk()
b = tk.Button(root,justify = LEFT)
photo = tk.PhotoImage(file="BadHombre.png")
b.config(image=photo,width="100",height="100")
#b.pack(side=LEFT)



root.geometry("1000x725")
root.mainloop()