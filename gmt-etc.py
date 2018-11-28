#Copyright 2018 Affonso Amendola
#Distributed under GPL V3 License, check the LICENSE file for more info.

#GMT Exposure Time Calculator

#TODO
#Mostly everything
#
#OpticalElement
#See if passlight is working correctly
#
#Create a parser for an opticalResponseFile (and a format for that file, for that matter)
#
#Add function for CCD random dark response.
#Add function for atmospheric effect.
#Add function to determine signal to noise ratio.

import numpy as np
import pysymphot as symphot

class OpticalElement:
	def __init__(self, opticalResponseFilename):
		#[opticalResponseFilename] = string (relative or absolute filename, please use relative, for the love of god.)
		#initializes an optical element, using an optical Response File
		self.opticalResponse = parseOpticalResponseFile(opticalResponseFilename)
	#end __init__

	def passLight(self, receivedField):
		#[receivedField] = Field object.
		#initializes a new field object that will be a modified version of the received field,
		#the modification made will be based on the optical response of this optical element,
		#interpolation will be used if there isnt data on the wavelength axis of the optical response
		#table for a set wavelength on the received field.
		self.field = Field(receivedField.resolution, receivedField.sizeX, receivedField.sizeY)
		for wavelength in receivedField.count_table.keys():
			self.field.Pythoncount_table[wavelength] = receivedField.count_table[wavelength]*interp(opticalResponse, wavelength)
	#end passLight
#end OpticalElement

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

		star_count_table = {}
		gaussian_image = create_gaussian(self.lengthX, self.lengthY, posX, posY, fwhm, 1.)

		for wavelength in spectrum.wave:
			star_count_table[wavelength] = gaussian_image*spectrum.sample(wavelength)
			count_table[wavelength] += star_count_table[wavelength]
	#end create_gaussian_star

	def create_gaussian(self, sizeX, sizeY, posX, posY, fwhm, height):
		distribution = np.array(np.zeros((sizeX, sizeY)))
		#creates a 2d gaussian distribution with fwhm and height on the field, at the pos(x,y).
		for i in range(sizeX):
			for j in range(sizeY):

				distribution[i][j] = height * np.exp( (-4.) * np.log(2.) * ((float(i)-posX)**2.+(float(j)-posY)**2.)  / fwhm**2.  )
	#end make_gaussian
#end Field 
#
#	Affonso was here.
#	Be excellent to each other.
# 
#	1:47:55, Wednesday, 28th of November, 2018, São Paulo, Brasil, Earth. 