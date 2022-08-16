from ctypes.wintypes import RECT
import tkinter as tk
import random
from turtle import Screen
import matplotlib
import ctypes
import sklearn
import numpy as np
from tkinter import *
from tkinter import colorchooser
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
from random import randrange, seed
from random import randint
import sys
import math
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

canvasDimension = 800

h_coord= []
v_coord=[]
oldPoints = []
side = 0
hGap = 0
rectPoints = []
triPoints = []
res_list = []
greenPoli = [(0, 0)]


user32 = ctypes.windll.user32

if(user32.GetSystemMetrics(0) == 2560 and user32.GetSystemMetrics(1) == 1440):
    canvasDimension=1000
    screenW=2000 
elif(user32.GetSystemMetrics(0) == 1280 and user32.GetSystemMetrics(1) == 720):
    canvasDimension=501
    screenW=1003

colors = [(126, 150, 194), '#7e96c2']

window = tk.Tk()
window.title("PolygonApp")
#geometry = "%dx%d" % (screenWidth, screenHeight)
#window.geometry(geometry)
window.grid_rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.attributes('-fullscreen',True)
l = tk.IntVar()

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
    de = [random.choice(h_coord) for _ in range(n)]
    
    de.sort()
    dep, dem = random_partition(de[1:-1])
    dem.reverse()
    des = [de[0]] + dep + [de[-1]] + dem + [de[0]]
    deltas = [des[i] - des[i-1] for i in range(1, len(des))]
    return deltas, (de[0], de[-1])

def get_xyq(n):
    
    print( '\n' '\n')
    
    x, (a1, a2) = get_deltas(n)
    y, (b1, b2) = get_deltas(n)
    
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
    points = [(p[0]+dx, p[1]+dy) for p in points]
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
    hGap = canvasDimension / gridDimension.get() #coordinate griglia
    vGap = canvasDimension / gridDimension.get()
    side = hGap
    n=1

    # Creates all vertical lines at intevals of hGap
    for i in range(0, canvasDimension, int(hGap)):
        h_coord.append(i)
    # Creates all horizontal lines at intevals of vGap
    for i in range(0, canvasDimension, int(vGap)):
        v_coord.append(i)
    
    dim = gridDimension.get()

    #Inizio algoritmo
    if len(sys.argv) == 2:
        dim = int(sys.argv[1])
    points = get_xyq(dim)

    #print("h_coord", h_coord)
    h_coord.clear() #reset h_coord
    #print("h_coord", h_coord)
    newPoints = points
    #print("NewPoints =\n", newPoints)
    
    NPDim = len(newPoints)
    if (NPDim % 2 != 0):
        newPoints.pop(1)
    c.create_polygon(newPoints, fill='red', width=2,)
    global oldPoints
    oldPoints = newPoints
    #print("OldPoints = ",oldPoints)
        # Creates all vertical lines at intevals of hGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(i, 0, i, canvasDimension, fill="black")
        
    # Creates all horizontal lines at intevals of vGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(0, i, screenW, i, fill="black")
        
class greenPoligon:
    coordinate = []

def refresh_grid():
    c.delete("all")
    hGap = canvasDimension / gridDimension.get() #coordinate griglia

    #print("refreshgrid oldPoints = ", oldPoints)
    greenPoli1 = greenPoligon()
    setattr(greenPoli1,'coordinate',res_list)

    
    #print("greenpoli1", greenPoli1)
    #print("greenpoli", greenPoli)

    # [(400, 800), (0, 600), (0, 400), (0, 0), (600, 200), (400, 800)]
    
    startingRectPoints = [(0, 0), (0, hGap), (hGap, hGap), (hGap, 0), (0, 0)]
    startingTriPoints = [(0, 0), (0, hGap), (hGap, hGap), (0, 0)]

    c.create_polygon(oldPoints, outline='', fill='red', width=2,)
    if(l.get() == 0):
        c.create_polygon(startingRectPoints, outline='', fill='green', width=2,)
        
    if(l.get() == 1):
        c.create_polygon(startingTriPoints, outline='', fill='green', width=2,)

    global rectPoints, triPoints
    rectPoints = startingRectPoints
    triPoints = startingTriPoints
    
    for i in range(1,len(greenPoli),1):
        z = id(greenPoli[i])
        print("z",z)
        a = ctypes.cast(z, ctypes.py_object).value
        print("a",a)
        antonio = list(a)
        print("antonio",antonio)
        c.create_polygon(antonio, outline='', fill='green', width=2,)
        

    #Create all green poly
    #for i in range(1, len(greenPoli), 1):
        #z = id(greenPoli[i])
        #a = ctypes.cast(z, ctypes.py_object).value
        #c.create_polygon(a.coordinate, outline='', fill='green', width=2,)
        #print("antoni0", a)
 

    # Creates all vertical lines at intevals of hGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(i, 0, i, canvasDimension, fill="black")
    # Creates all horizontal lines at intevals of vGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(0, i, screenW, i, fill="black")
   
def move_down():
    c.delete("all")
    hGap = canvasDimension / gridDimension.get() #coordinate griglia
    control = True
    global res_list, rectPoints, triPoints

    if(l.get() == 0):
        xCoord, yCoord = zip(*rectPoints)
        res_list = list(rectPoints)
    else:
        xCoord, yCoord = zip(*triPoints)
        res_list = list(triPoints)

    
    temp_list = res_list
   

    for i in range (0, len(temp_list), 1):
        temp_list[i] = (xCoord[i], yCoord[i] + hGap)

    for i in range (0, len(yCoord), 1):
        if(yCoord[i] >= canvasDimension):
            control = False
            messagebox.showinfo(title = 'Error', message = '- - - Wrong coordinates- - - ')
            break

    if (control == True):
        res_list = temp_list
        c.create_polygon(oldPoints, outline='', fill='red', width=2,)
        c.create_polygon(res_list, outline='', fill='green', width=2,)
    else:
        move_up()
        c.create_polygon(oldPoints, outline='', fill='red', width=2,)
        c.create_polygon(res_list, outline='', fill='green', width=2,)
 
    #c.create_polygon(res_list, outline='', fill='green', width=2,)
    if(l.get() == 0):
        rectPoints = res_list
    else:
        triPoints = res_list
    
    # Creates all vertical lines at intevals of hGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(i, 0, i, canvasDimension, fill="black")
    # Creates all horizontal lines at intevals of vGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(0, i, screenW, i, fill="black")

def move_up():
    c.delete("all")
    hGap = canvasDimension / gridDimension.get() #coordinate griglia
    control = True
    global res_list, rectPoints, triPoints
    

    if(l.get() == 0):
        xCoord, yCoord = zip(*rectPoints)
        res_list = list(rectPoints)
    else:
        xCoord, yCoord = zip(*triPoints)
        res_list = list(triPoints)

    temp_list = res_list
   

    for i in range (0, len(temp_list), 1):
        temp_list[i] = (xCoord[i], yCoord[i] - hGap)

    for i in range (0, len(yCoord), 1):
        if(yCoord[i] <= 0):
            control = False
            messagebox.showinfo(title = 'Error', message = '- - - Wrong coordinates- - - ')
            break

    if (control == True):
        res_list = temp_list
        c.create_polygon(oldPoints, outline='', fill='red', width=2,)
        c.create_polygon(res_list, outline='', fill='green', width=2,)
    else:
        move_down()
        c.create_polygon(oldPoints, outline='', fill='red', width=2,)
        c.create_polygon(res_list, outline='', fill='green', width=2,)
 
    #c.create_polygon(res_list, outline='', fill='green', width=2,)
 
    if(l.get() == 0):
        rectPoints = res_list
    else:
        triPoints = res_list
    # Creates all vertical lines at intevals of hGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(i, 0, i, canvasDimension, fill="black")
    # Creates all horizontal lines at intevals of vGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(0, i, screenW, i, fill="black")


def move_right():
    c.delete("all")
    hGap = canvasDimension / gridDimension.get() #coordinate griglia
    control = True
    global res_list, rectPoints, triPoints
    if(l.get() == 0):
        xCoord, yCoord = zip(*rectPoints)
        res_list = list(rectPoints)
    else:
        xCoord, yCoord = zip(*triPoints)
        res_list = list(triPoints)

    temp_list = res_list
   

    for i in range (0, len(temp_list), 1):
        temp_list[i] = (xCoord[i] + hGap, yCoord[i])

    for i in range (0, len(xCoord), 1):
        if(xCoord[i] >= canvasDimension):
            control = False
            messagebox.showinfo(title = 'Error', message = '- - - Wrong coordinates- - - ')
            break

    if (control == True):
        res_list = temp_list
        c.create_polygon(oldPoints, outline='', fill='red', width=2,)
        c.create_polygon(res_list, outline='', fill='green', width=2,)
    else:
        move_left()
        c.create_polygon(oldPoints, outline='', fill='red', width=2,)
        c.create_polygon(res_list, outline='', fill='green', width=2,)
 
    #c.create_polygon(res_list, outline='', fill='green', width=2,)
 
    if(l.get() == 0):
        rectPoints = res_list
    else:
        triPoints = res_list

    # Creates all vertical lines at intevals of hGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(i, 0, i, canvasDimension, fill="black")
    # Creates all horizontal lines at intevals of vGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(0, i, screenW, i, fill="black")


def move_left():
    c.delete("all")
    hGap = canvasDimension / gridDimension.get() #coordinate griglia
    control = True
    global res_list, rectPoints, triPoints
    if(l.get() == 0):
        xCoord, yCoord = zip(*rectPoints)
        res_list = list(rectPoints)
    else:
        xCoord, yCoord = zip(*triPoints)
        res_list = list(triPoints)
    temp_list = res_list
   
    print("TempList[] = ", temp_list)
    for i in range (0, len(temp_list), 1):
        temp_list[i] = (xCoord[i] - hGap, yCoord[i])

    for i in range (0, len(xCoord), 1):
        if(xCoord[i] <= 0):
            control = False
            messagebox.showinfo(title = 'Error', message = '- - - Wrong coordinates- - - ')
            break

    if (control == True):
        res_list = temp_list
        c.create_polygon(oldPoints, outline='', fill='red', width=2,)
        c.create_polygon(res_list, outline='', fill='green', width=2,)
    else:
        move_right()
        c.create_polygon(oldPoints, outline='', fill='red', width=2,)
        c.create_polygon(res_list, outline='', fill='green', width=2,)
 
    #c.create_polygon(res_list, outline='', fill='green', width=2,)
 
    if(l.get() == 0):
        rectPoints = res_list
    else:
        triPoints = res_list
    # Creates all vertical lines at intevals of hGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(i, 0, i, canvasDimension, fill="black")
    # Creates all horizontal lines at intevals of vGap
    for i in range(0, canvasDimension, int(hGap)):
        c.create_line(0, i, screenW, i, fill="black")

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
c = Canvas(GamePage, bg="white", height=canvasDimension, width=canvasDimension) #cambiato solo screenW in screenH
tag_name = "polygon"

gridDimension = Scale(GamePage, from_=5, to=20, orient=HORIZONTAL, label= "Cells")
#draw_grid()
startButton = tk.Button(GamePage, text="Start", command= draw_grid)

drawButton = tk.Button(GamePage, text="Draw", command= refresh_grid) # command= refresh_grid()

upButton = tk.Button(GamePage, text="Up", command = move_up)

downButton = tk.Button(GamePage, text="Down", command = move_down)

rightButton = tk.Button(GamePage, text="Right", command = move_right)

leftButton = tk.Button(GamePage, text="Left", command = move_left)

doneButton = tk.Button(GamePage, text="Done")

rectangle = tk.Radiobutton(GamePage, text="Rectangle", variable=l, value=0)
#rectBase = Scale(GamePage, from_=1, to=10, orient=HORIZONTAL, label="Base")
#rectHeight = Scale(GamePage, from_=1, to=10, orient=HORIZONTAL, label="Height")
triangle = tk.Radiobutton(GamePage, text="Triangle", variable=l, value=1)
#triBase = Scale(GamePage, from_=1, to=10, orient=HORIZONTAL, label="Base")
#triHeight = Scale(GamePage, from_=1, to=10, orient=HORIZONTAL, label="Height")
gameBackButton = tk.Button(GamePage, text = "Menu", command = menuFromGame)

c.grid(sticky="NW", rowspan=2, columnspan=2, padx=(30,0), pady=(30,0))
gridDimension.grid(sticky="SW", row=0, column=2, pady=30)
startButton.grid(sticky="NW", row=1, column=2)
rectangle.grid( row=2, column=0, padx=200, pady=(0,0))
drawButton.grid(row=3, column=0, padx=200, pady=(0,0))

upButton.grid(sticky="N",row=0, column=1, pady=(300,0))

downButton.grid(sticky="S", row=0, column=1, pady=(0,300))

rightButton.grid(sticky="E",row=0, column=1, padx = (0, 350))

leftButton.grid(sticky="W", row=0, column=1, padx = (350, 0))

triangle.grid(sticky="W", row=2, column=1)

gameBackButton.grid(sticky="EW", row=4, column=2, padx=30)




MenuPage.pack(fill = BOTH, expand = True)
window.mainloop()