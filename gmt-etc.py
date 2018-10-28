#Copyright 2018 Affonso Amendola
#Distributed under GPL V3 License, check the LICENSE file for more info.

#GMT Exposure Time Calculator

import numpy as np
import pysymphot as symphot

class Field:
	def __init__(self, resolution, sizeX, sizeY):
		#initializes field object, with an array of size/resolution on x and y
		#[resolution] = pixels/arcmin
		#[sizeX] and [sizeY] = arcmin

		self.resolution = resolution
		self.sizeX = sizeX
		self.sizeY = sizeY

		self.count_table = {} 

		self.lengthX = int(resolution*sizeX)
		self.lengthY = int(resolution*sizeY)

	#end __init__

	def create_gaussian_star(self, posX, posY, fwhm, spectrum):
		# [spectrum] = Pysynphot Source Object
		# [posX]. [posY] = pixel position (int)
		# 
		# Convolves a gaussian bidimensional image with a template spectrum, basically
		# the star with that spectrum at (posX, posY) in the field.
		# 
		# I think thats how it works...

		gaussian_image = create_gaussian(self.lengthX, self.lengthY, posX, posY, fwhm, 1.)

		for wavelength in spectrum.wave:
			count_table[wavelength] = gaussian_image*spectrum.sample(wavelength)


	#end create_gaussian_star

	def get_counts_at(self, posX, posY):

	#end get_counts_at

	def create_gaussian(self, sizeX, sizeY, posX, posY, fwhm, height):
		distribution = np.array(np.zeros((sizeX, sizeY)))
		#creates a 2d gaussian distribution with fwhm and height on the field, at the pos(x,y).
		for i in range(sizeX):
			for j in range(sizeY):

				distribution[i][j] = height * np.exp( (-4.) * np.log(2.) * ((float(i)-posX)**2.+(float(j)-posY)**2.)  / fwhm**2.  )
	#end make_gaussian

def count_per_res_element(	field, filter
				  			exposure_time, efficiency, telescope_surface, photon_energy):
	

#end count_per_res

def out_matrix_file(filename, matrix):

	f = open(filename, "w")

	for i in range( len(matrix) ):
		for j in range( len(matrix[i]) ):

			f.write( str(matrix[i][j]) )
			f.write(" ")

		f.write("\n")

#end out_matrix_file


