import tkinter as tk

app = tk.Tk()

label = tk.Label(app, text="Hello!", font=("Arial",64))
label.pack()

def clickedButton():
    label["text"] = "CLICKED!"
    #inputText = textbox.get()
    #if not inputText.isdigit():
     #   label["text"] = "Not a digit!!! Retry!"
    #else:
     #   label["text"] = "Thanks"

button = tk.Button(app, text="Click me!", command=clickedButton)
button.pack()

canvas = tk.Canvas(app, width=400, height=300, bg="gray")
canvas.pack()
canvas.create_oval(150,150,200,200, tag="circle")
vx = 15
vy = 0
def keyPress(event):
    global vy
    vy = vy + 3


def drawFrame():
    global vx, vy
    canvas.move("circle", vx, vy)

    if(canvas.coords("circle")[0] > 350):
        vx = -vx
    elif(canvas.coords("circle")[0] < 10):
        vx = -vx

    if(canvas.coords("circle")[1]>250):
        vy = -vy
    elif(canvas.coords("circle")[1] < 10):
        vy = -vy
    app.after(10, drawFrame)


app.bind("<KeyPress>", keyPress)

canvas.after(10,drawFrame)
app.geometry("800x600")
app.mainloop()