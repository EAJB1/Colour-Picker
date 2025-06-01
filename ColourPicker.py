from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkcolorpicker import askcolor

from pynput import mouse
from pynput.mouse import Controller

from PIL import ImageGrab

import pygetwindow as gw

import time

mouseOperator = Controller()
positionDelta = 5
lastMousePosition = (0, 0)
mouseUpdateTime = 0.1
clicked = False

colour = '#%02x%02x%02x' % (200, 50, 50)
r,g,b = 200,50,50

def GetHex(rgb):
    return '%02X%02X%02X'%rgb

def GetColour(x, y):
    global colour
    global r,g,b

    im = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    rgbim = im.convert('RGB')
    r,g,b = rgbim.getpixel((0,0))
    colour = '#%02x%02x%02x' % (r, g, b)
    
    print(f'COLOR: rgb{(r,g,b)} | HEX #{GetHex((r,g,b))}')

def OnMove(x, y):
    GetColour(x,y)

def OnClick(x,y, button, pressed):
    global clicked
    global win

    if pressed and button == mouse.Button.left:
        GetColour(x, y)
        clicked = True
        return False

def Listen():
    with mouse.Listener(on_click=OnClick) as listener:
        listener.join()
    
    Update()

def Update():
    global lastMousePosition
    global clicked

    while True:
        if clicked == True:
            clicked = False
            break

        x, y = mouseOperator.position
        if abs(x - lastMousePosition[0]) > positionDelta or \
           abs(y - lastMousePosition[1]) > positionDelta:
            lastMousePosition = (x, y)
            print("Mouse Pos: ",lastMousePosition)

            GetColour(x, y)
            break

        time.sleep(mouseUpdateTime)
    
    SetColour()
    Front()
    root.mainloop()

def Front():
    win = gw.getWindowsWithTitle('Colour Picker')[0]
    #print("Window: ",win)
    gw.Win32Window.activate(win)

def Edit():
    global colour
    global r,g,b
    
    tuple = askcolor((r,g,b), root, "Edit Colour", False)
    
    if tuple[1] != None:
        (r,g,b) = tuple[0]
        colour = tuple[1]
        SetColour()

def Main():
    SetColour()
    root.mainloop()

root = tk.Tk()
root.title('Colour Picker')
root.geometry('250x145')
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use('clam')

def SetColour():
    global colour
    print("Set to: ",colour)
    c.config(bg=colour)
    
    rgb_t.config(state=tk.NORMAL)
    rgb_t.delete('1.0', tk.END)
    rgb_t.insert(tk.END, f"{r,g,b}")
    rgb_t.config(state=tk.DISABLED)

    hex_t.config(state=tk.NORMAL)
    hex_t.delete('1.0', tk.END)
    hex_t.insert(tk.END, f"#{GetHex((r,g,b))}")
    hex_t.config(state=tk.DISABLED)

button = tk.Button(root, text='Pick', command=Listen)
button.grid(row=0, column=0, padx=0, pady=2)

button3 = tk.Button(root, text='Edit', command=Edit)
button3.grid(row=0, column=1, padx=0, pady=2)

c = Canvas(root, bg="white", height=25, width=245)
c.grid(row=1, column=0, columnspan=2, padx=0)

rgb_lb = tk.Label(root, text="RGB:")
rgb_lb.grid(row=2, column=0, columnspan=2)

rgb_t = Text(root, height=1, width=30)
rgb_t.insert(1.0, " ")
rgb_t.config(state=tk.DISABLED)
rgb_t.grid(row=3, column=0, columnspan=2)

hex_lb = tk.Label(root, text="HEX:")
hex_lb.grid(row=4, column=0, columnspan=2)

hex_t = Text(root, height=1, width=30)
hex_t.insert(1.0, " ")
hex_t.config(state=tk.DISABLED)
hex_t.grid(row=5, column=0, columnspan=2)

if __name__ == "__main__":
    Main()