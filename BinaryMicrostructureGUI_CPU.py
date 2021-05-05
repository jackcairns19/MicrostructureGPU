#!/usr/bin/env python
import os
os.environ["OMP_NUM_THREADS"] = '20' # export OMP_NUM_THREADS=4
os.environ["OPENBLAS_NUM_THREADS"] = '20' # export OPENBLAS_NUM_THREADS=4
os.environ["MKL_NUM_THREADS"] = '20' # export MKL_NUM_THREADS=6
from tkinter import *
from PIL import ImageTk
import numpy as np
from threadpoolctl import threadpool_limits
from scipy.optimize import brentq
from PIL import Image
np.show_config()

def getMicrostructure(liquidFraction, moleFraction):
	
	"""
	Return a primary microstructure image with liquidFraction (in range [0,1]) and moleFraction (in range [0,1]).
	"""
	assert(0.<=liquidFraction and liquidFraction<=1)
	assert(0.<=moleFraction and moleFraction<=1)
	#Image paramters:
	N = 1024 #image dimensions
	nGrains = 10 #max number of grains shown
	liquidColor = np.array([200,200,255], dtype=np.uint8) #color within liquid region
	solidColor = np.array([100,100,255], dtype=np.uint8) #color within grains
	edgeColor = np.array([0,0,0], dtype=np.uint8) #color of grain boundary lines

	#Initialize grid:
	with threadpool_limits(limits=16, user_api='openmp'):	
		np.random.seed(0)
		x = np.array(np.meshgrid(range(N), range(N))) #grid
		x0 = np.random.rand(2,nGrains)*N #seed locations for each grain
		rAvg = np.sqrt(N*N/(np.pi*nGrains)) #avg grain radius in full solid
		r0 = (np.random.rand(nGrains)*moleFraction + np.random.rand(nGrains)*(1-moleFraction))*rAvg #nucleation time, converted to radius using growth rate
		r0 -= r0.min() #Without loss of generality earliest grain nucleates at t=0
		rDiff = np.linalg.norm(x[:,None]-x0[:,:,None,None], axis=0) + r0[:,None,None] #time at which each grain would reach each pixel (if no other grains were present)
		grainID = np.argmin(rDiff, axis=0) #determine which grain will get to each pixel first
		rMin = np.min(rDiff, axis=0) #r at which each pixel would become part of a grain (liquid before)
		
		#Find time to match specified liquidFraction:
		dA = 1./(N*N) #Area integration factor
		def liquidFractionError(r):
			return np.count_nonzero(r < rMin)*dA - liquidFraction

			
		r = brentq(liquidFractionError, 0, 1.42*N, xtol=1.) #find r to 1-pixel accuracy to match liquidFraction
		grainID[np.where(r < rMin)] = -1 #liquid region
		edges = np.where(np.logical_or(
		grainID[:-1,:-1]!=grainID[1:,:-1],
		grainID[:-1,:-1]!=grainID[:-1,1:])) #detect grain boundaries

	#Convert to image
	pixels = np.tile(solidColor[None,None,:], (N,N,1))
	pixels[np.where(grainID<0)] = liquidColor
	pixels[edges] = edgeColor
	return Image.fromarray(pixels)
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





