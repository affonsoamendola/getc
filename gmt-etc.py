#Copyright 2018 Affonso Amendola
#Distributed under GPL V3 License, check the LICENSE file for more info.

#GMT Exposure Time Calculator

import numpy as np

class Field:
	def __init__(self, resolution, sizeX, sizeY):
		#initializes field object, with an array of size/resolution on x and y, everything in arcmin 
		self.resolution = resolution
		self.sizeX = sizeX
		self.sizeY = sizeY

		self.lengthX = int(sizeX/resolution)
		self.lengthY = int(sizeY/resolution)

		self.flux = np.array(np.empty((self.lengthX, self.lengthY))) 

	def make_gaussian(self, posX, posY, fwhm, height):
		
		for i in range(self.lengthX):
			for j in range(self.lengthY):

				self.flux[i][j] = height * np.exp( (-4.) * np.log(2.) * ((float(i)-posX)**2.+(float(j)-posY)**2.)  / fwhm**2.  )

OBSERVATION_MODE_IMAGING = 0
OBSERVATION_MODE_SPECTROSCOPY = 1

SOURCE_TYPE_POINT = 0
SOURCE_TYPE_EXTENDED = 1

def count_per_res(	observation_mode, source_type, incident_flux, filter_band_width, 
				  	exposure_time, efficiency, telescope_surface, photon_energy):	
	if(observation_mode == OBSERVATION_MODE_IMAGING):
		if(source_type == SOURCE_TYPE_POINT):
			N = (incident_flux*filter_band_width*exposure_time*efficiency*telescope_surface)/photon_energy
			return N
	#elif(observation_mode == OBSERVATION_MODE_SPECTROSCOPY):

def out_matrix_file(filename, matrix):
	f = open(filename, "w")
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			f.write(str(matrix[i][j]))
			f.write(" ")
		f.write("\n")

field = Field(0.1, 10, 10)
field.make_gaussian(10.,10.,1.,100.)

out_matrix_file("matrixout.txt", field.flux)


