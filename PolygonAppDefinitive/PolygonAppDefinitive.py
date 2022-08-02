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
import sys
import math
import matplotlib.pyplot as plt
import 



screenH = 752
screenW = 1504
user32 = ctypes.windll.user32
if(user32.GetSystemMetrics(0) == 2560 and user32.GetSystemMetrics(1) == 1440):
    screenH=1000
    screenW=2000 
elif(user32.GetSystemMetrics(0) == 1280 and user32.GetSystemMetrics(1) == 720):
    screenH=501
    screenW=1003

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
def random_partition(a):
    b = list()
    c = list()
    for i in range(len(a)):
        if random.randrange(2):
            b.append(a[i])
        else:
            c.append(a[i])
    return b, c

def get_deltas(n):
    de = [random.random() for _ in range(n)]
    print('\n', de)
    de.sort()
    dep, dem = random_partition(de[1:-1])
    dem.reverse()
    des = [de[0]] + dep + [de[-1]] + dem + [de[0]]
    deltas = [des[i] - des[i-1] for i in range(1, len(des))]
    return deltas, (de[0], de[-1])

def get_xyq(n, x, y):
    print (x)
    print( '\n' '\n')
    
    x, (a1, a2) = get_deltas(n)
    y, (b1, b2) = get_deltas(n)
    print (x)
    random.shuffle(y)
    vectors = [(x[i], y[i]) for i in range(n)]
    vectors.sort(key=lambda v: math.atan2(v[1], v[0]))
    points = [(0, 0)]
    for v in vectors:
        points.append((points[-1][0] + v[0], points[-1][1] + v[1]))
    xmin = min([p[0] for p in points])
    ymin = min([p[1] for p in points])
    dx = a1 - xmin
    dy = b1 - ymin
    points = np.array([(p[0]+dx, p[1]+dy) for p in points])
    print("\n", points)
    return points

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
    hGap = screenW / gridDimension.get() #coordinate griglia
    vGap = screenH / gridDimension.get()

    h_coord= []
    v_coord=[]
    n=1

    #coordinate x e y
    y = []
    x = []

    # Creates all vertical lines at intevals of hGap
    for i in range(0, screenW, int(hGap)):
        c.create_line(i, 0, i, screenH, fill="black")
        h_coord.append(i)
    # Creates all horizontal lines at intevals of vGap
    for i in range(0, screenH, int(vGap)):
        c.create_line(0, i, screenW, i, fill="black")
        v_coord.append(i)
    
    dim = gridDimension.get() * gridDimension.get()

    #Inizio algoritmo
    if len(sys.argv) == 2:
        dim = int(sys.argv[1])
    points = get_xyq(dim, h_coord, v_coord)

    vector1 = []
    vector2 = []
    #split points into two different arrays
    for x, y in points:
        vector1.append(x)
        vector2.append(y)

    vector1 = vector1.inverse_transform
    vector2 = vector2 * 1000
    print("\n", vector1)
    print("\n", vector2)
    qwerty = len(vector1)

    if (qwerty %2 != 0):
        vector1 = vector1.pop()
    for q in range(0, 1, len(vector1)):
        c.create_polygon(vector1[q],vector2[q], outline='#f11', fill='red', width=2)
        
    
    #c.create_line(p[0] for p in points], [p[1] for p in points], outline='#f11', fill='red', width=2)
     

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
c = Canvas(GamePage, bg="white", height=screenH, width=screenW)
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