import tkinter as tk
import random
import ctypes
import numpy as np
from tkinter import *
from tkinter import colorchooser
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
from random import seed
from random import randint



a = 752
b = 1504
user32 = ctypes.windll.user32
if(user32.GetSystemMetrics(0) == 2560 and user32.GetSystemMetrics(1) == 1440):
    a=1000
    b=2000 
elif(user32.GetSystemMetrics(0) == 1280 and user32.GetSystemMetrics(1) == 720):
    a=501
    b=1003

colors = [(126, 150, 194), '#7e96c2']

window = tk.Tk()
window.title("PolygonApp")
#geometry = "%dx%d" % (screenWidth, screenHeight)
#window.geometry(geometry)
window.grid_rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.attributes('-fullscreen',True)

#Menu Page
MenuPage = tk.Frame(window, bg = colors[1], )
MenuPage.grid_rowconfigure(0, weight=1)
MenuPage.grid_rowconfigure(1, weight=1)
MenuPage.grid_rowconfigure(2, weight=1)
MenuPage.grid_rowconfigure(3, weight=1)
MenuPage.grid_columnconfigure(0, weight=1)
#Image
logo = Image.open('logo.png')
logo = logo.convert("RGBA")
resizedLogo = logo.resize((442,100), Image.ANTIALIAS)
newLogo = ImageTk.PhotoImage(resizedLogo)
logo_label = tk.Label(MenuPage, image = newLogo)
logo_label.image = newLogo

#Options Page
OptionsPage = tk.Frame(window, bg = colors[1])
OptionsPage.grid_rowconfigure(0, weight=1)
OptionsPage.grid_rowconfigure(1, weight=1)
OptionsPage.grid_rowconfigure(2, weight=1)
OptionsPage.grid_columnconfigure(0, weight=1)

#GamePage
GamePage = tk.Frame(window, bg = colors[1])
GamePage.grid_rowconfigure(0, weight=1, pad=7)
GamePage.grid_rowconfigure(1, weight=1, pad=7)
GamePage.grid_rowconfigure(2, weight=1, pad=7)
GamePage.grid_rowconfigure(3, weight=1, pad=7)
GamePage.grid_rowconfigure(4, weight=1, pad=7)
GamePage.grid_columnconfigure(0, weight=1)
GamePage.grid_columnconfigure(1, weight=1, pad=7)
GamePage.grid_columnconfigure(2, weight=1, pad=7)
l = tk.IntVar();


#Methods
def optionsFrame():
    MenuPage.pack_forget()
    OptionsPage.pack(expand = True, fill = "both")

def gameFrame():
    MenuPage.pack_forget()
    GamePage.pack(expand = True, fill = "both")

def menuFromGame():
    GamePage.pack_forget()
    MenuPage.pack(expand = True, fill = "both")

def menuFromOptions():
    OptionsPage.pack_forget()
    MenuPage.pack(expand = True, fill = "both")

def change_color():
    colors = askcolor(title = "Colors")
    MenuPage.config(bg = colors[1])
    OptionsPage.config(bg = colors[1])
    GamePage.config(bg = colors[1])

def exit():
    window.destroy()

def draw_grid():
    c.delete("all")
    hGap = b / gridDimension.get() #coordinate griglia
    vGap = a / gridDimension.get()

    h_coord= []
    v_coord=[]
    n=1
    y = []
    x = []
    dim = gridDimension.get() * gridDimension.get()
   

    # Creates all vertical lines at intevals of hGap
    for i in range(0, b, int(hGap)):
        c.create_line(i, 0, i, a, fill="black")
        h_coord.append(i)
    # Creates all horizontal lines at intevals of vGap
    for i in range(0, a, int(vGap)):
        c.create_line(0, i, b, i, fill="black")
        v_coord.append(i)

    #i numeri dei lati devono essere pari. metto controllo per non farmi rompere
    while(n%2) != 0:
         n = np.random.randint(0, dim) #numero di lati del poligono

    for i in range(0,n):
        x.append(random.choice(h_coord))
        y.append(random.choice(v_coord))
    #x.sort()
    #y.sort()
    

    
    c.create_polygon(list(x),list(y), outline='#f11', fill='red', width=2)
    #c.create_line(x[i],y[i],x[i],y[i], fill="red", width=10)
        

def check_hand_enter():
    c.config(cursor="hand1")


def check_hand_leave():
    c.config(cursor="")

#Menu Widgets
playButton = tk.Button(MenuPage, text = "Play", command = gameFrame)
optionsButton = tk.Button(MenuPage, text = "Options", command = optionsFrame)
exitButton = tk.Button(MenuPage, text = "Exit", command = exit)

logo_label.grid(row=0, column=0, pady=20, padx=0)
playButton.grid(row=1, column=0, pady=(50,0), padx=0)
optionsButton.grid(row=2, column=0, pady=100, padx=0)
exitButton.grid(row=3, column=0, pady=(0,100), padx=0)

#Options Widgets
backgroundButton = tk.Button(OptionsPage, text="Background", command = change_color)
optBackButton = tk.Button(OptionsPage, text="Back", command = menuFromOptions)

backgroundButton.grid(column=0, row=0)
optBackButton.grid(column=0, row=1)

#Game Widgets
c = Canvas(GamePage, bg="white", height=a, width=b)
tag_name = "polygon"
c.create_polygon((100, 100), (25, 100), (125, 100), (125, 25), outline='black', fill="black", tag=tag_name)
c.tag_bind(tag_name, "<Enter>", lambda event: check_hand_enter())
c.tag_bind(tag_name, "<Leave>", lambda event: check_hand_leave())
gridDimension = Scale(GamePage, from_=5, to=20, orient=HORIZONTAL, label= "Cells")
draw_grid()
drawGrid = tk.Button(GamePage, text="Draw", command= draw_grid)
rectangle = tk.Radiobutton(GamePage, text="Rectangle", variable=l, value=0)
rectBase = Scale(GamePage, from_=1, to=10, orient=HORIZONTAL, label="Base")
rectHeight = Scale(GamePage, from_=1, to=10, orient=HORIZONTAL, label="Height")
triangle = tk.Radiobutton(GamePage, text="Triangle", variable=l, value=1)
triBase = Scale(GamePage, from_=1, to=10, orient=HORIZONTAL, label="Base")
triHeight = Scale(GamePage, from_=1, to=10, orient=HORIZONTAL, label="Height")
gameBackButton = tk.Button(GamePage, text = "Menu", command = menuFromGame)

c.grid(sticky="NW", rowspan=2, columnspan=2, padx=(30,0), pady=(30,0))
gridDimension.grid(sticky="SW", row=0, column=2, pady=30)
drawGrid.grid(sticky="NW", row=1, column=2)
rectangle.grid( row=2, column=0, padx=200, pady=(0,0))
rectBase.grid(row=3, column=0, padx=200, pady=(0,0))
rectHeight.grid(row=4, column=0, padx=200, pady=(0,30))
triangle.grid(sticky="W", row=2, column=1)
triBase.grid(sticky="W" ,row=3, column=1)
triHeight.grid(sticky="W" ,row=4, column=1, pady=(0, 30))
gameBackButton.grid(sticky="EW", row=4, column=2, padx=30)


MenuPage.pack(fill = BOTH, expand = True)
window.mainloop()