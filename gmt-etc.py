#Copyright 2018 Affonso Amendola
#Distributed under GPL V3 License, check the LICENSE file for more info.

#GMT Exposure Time Calculator

#TODO
#Mostly everything
#
#OpticalElement
#See if passlight is working correctly
#
#Add function for CCD random dark response.
#Add function for atmospheric effect.
#Add function to determine signal to noise ratio.

import numpy as np
import pysymphot as symphot


def parseOpticalResponseFile(opticalResponseFilename):
	#[opticalResponseFilename] = string (relative or absolute filename, please use relative, for the love of god.)
	#Reads a .tab file containing the optical response of a certain optical element, two columns, 
	#separated by a \t column 0 contains a wavelength, and column 1 contains the Reflectivity or Transmissivity, 
	#on the element type.
	
	table = np.loadtxt(opticalResponseFilename, delimiter="\t", usecols=(0,1))
	return table

#end parseOpticalResponseFile

class Optical_Element:
	def __init__(self, opticalResponseFilename):
		#[opticalResponseFilename] = string (relative or absolute filename, please use relative, for the love of god.)
		#initializes an optical element, using an optical Response File

		self.opticalResponse = parseOpticalResponseFile(opticalResponseFilename)
	
	#end __init__

	def passLight(self, spectrum):
		#[spectrum_counts] = Spectrum Table (x value = wavelength, y value = counts)
 
		return_spectrum = Spectrum()

		for wavelength in spectrum:
			return_spectrum.set_counts_for_wavelength(wavelength, spectrum.get_counts_for_wavelength(wavelength)*interp(opticalResponse, wavelength))
		
		return return_spectrum

	#end passLight
#end Optical_Element

class Instrument:
	Optical_Element_List = []

	def __init__(self):

	def Add_Optical_Element(self, Optical_Element):
		Optical_Element_List.append(Optical_Element)

	def Pass_Light(self, start_spectrum):

	def Calculate_SNR(self):

class Spectrum:
	def __init__(self):
		self.spectrum_wavelength = []
		self.spectrum_counts = []

	def get_counts_for_wavelength(self, wavelength):

	def load_spectrum_from_file(self, filename):


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


#	Affonso was here,
#	Be excellent to each other.
# 
#	1:47:55, Wednesday, 28th of November, 2018, São Paulo, Brasil, Earth. 