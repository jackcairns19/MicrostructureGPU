#!/usr/bin/env python
from PIL import Image
import numpy as np
from scipy.optimize import brentq
import time

#You may directly call this function and get an image in memory to serve on the webpage
#Alternately, you can run the python script as an executable and write an image to disk


def getMicrostructure(liquidFraction, moleFraction):
	"""
	Return a primary microstructure image with liquidFraction (in range [0,1]) and moleFraction (in range [0,1]).
	"""
	t0 = time.time()
	assert(0.<=liquidFraction and liquidFraction<=1)
	assert(0.<=moleFraction and moleFraction<=1)
	
	#Image paramters:
	N = 1024 #image dimensions
	nGrains = 10 #max number of grains shown
	liquidColor = np.array([200,200,255], dtype=np.uint8) #color within liquid region
	solidColor = np.array([100,100,255], dtype=np.uint8) #color within grains
	edgeColor = np.array([0,0,0], dtype=np.uint8) #color of grain boundary lines
	
	#Initialize grid:
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
	print(time.time() - t0)
	return Image.fromarray(pixels)

#Handle executable mode: write image to specified file (any extension supported by PIL; includes png, jpg etc.)
if __name__=="__main__":
	import sys
	if len(sys.argv) != 4:
		print('Usage: BinaryMicrostructure.py <liquidFraction> <moleFraction> <fileName>')
		exit(1)
	liquidFraction = float(sys.argv[1])
	moleFraction = float(sys.argv[2])
	fileName = sys.argv[3]
	getMicrostructure(liquidFraction, moleFraction).save(fileName)
