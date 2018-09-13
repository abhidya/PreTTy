import tkinter as tk


root = tk.Tk()
logo = tk.PhotoImage(file="~/Pictures/supremeLord.gif")

w1 = tk.Label(root, image=logo).pack(side="right")



w2 = tk.Label(root, justify=tk.LEFT, padx = 10,
			text="Hello Tkinter!").pack(side="left")
root.mainloop()
