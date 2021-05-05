#!/usr/bin/env python
from tkinter import *
from PIL import ImageTk
from BinaryMicrostructure import getMicrostructure

#Create window:
root = Tk()
root.title('Binary microstructure')
root.geometry('1268x1028+300+300')
root.resizable(0,0)

#Create widget to show image:
img = ImageTk.PhotoImage(getMicrostructure(0.5,0.5))
lblImg = Label(root, image=img)
lblImg.pack(side=LEFT)

#Routine to update image:
def update(val):
	liquidFraction = sclLiquidFraction.get()
	moleFraction = sclMoleFraction.get()
	img = ImageTk.PhotoImage(getMicrostructure(liquidFraction, moleFraction))
	lblImg.configure(image=img)
	lblImg.image = img

#Create controllers
frame = Frame(root)
sclLiquidFraction = Scale(frame, from_=0.0, to=1.0, resolution=0.01, label='Liquid fraction', orient=HORIZONTAL, length=200, command=update)
sclLiquidFraction.set(0.5)
sclLiquidFraction.pack(side=TOP)
sclMoleFraction = Scale(frame, from_=0.0, to=1.0, resolution=0.01, label='Mole fraction', orient=HORIZONTAL, length=200, command=update)
sclMoleFraction.set(0.5)
sclMoleFraction.pack(side=TOP, pady=20)
frame.pack(side=LEFT, padx=10)

root.mainloop()


