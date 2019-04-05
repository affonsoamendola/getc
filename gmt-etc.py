#Copyright 2018 Affonso Amendola
#Distributed under GPL V3 License, check the LICENSE file for more info.

#GMT Exposure Time Calculator

import numpy as np

from astropy.modeling.blackbody import blackbody_lambda
from astropy.constants import h, c
from astropy import units

VERSION = 0.01

SOURCE_TYPE = "point"
OBSERVATION_MODE = "imaging"

flux_input_type = "a"

temperature = units.K * 5000

flux_template = ""
redshift = 0

reference_wavelength = 0
power_law_index = 0
reference_flux = 0

line_central_wavelength = 0
line_fwhm = 0
line_total_flux = 0

observed_wavelength = units.micrometer * 500

filter_band_width = 0
spectral_bin = 0

telescope_surface = 0
exposure_time = 0
efficiency = 0

flux_unit = units.joule * (units.second**-1) * (units.meter**-2) * (units.micrometer**-1) * (units.sr**-1)

def user_input():
	global SOURCE_TYPE
	global OBSERVATION_MODE

	global flux_input_type
	global temperature

	global flux_template
	global redshift
	global reference_wavelength
	global power_law_index
	global reference_flux
	global line_central_wavelength
	global line_fwhm
	global line_total_flux
	global observed_wavelength

	global filter_band_width
	global spectral_bin

	global telescope_surface
	global exposure_time
	global efficiency

	print("--------------------------------------------------------------")
	print("GMT-ETC ver. ", VERSION)
	print("Made by Affonso Amendola, under request and orientation of Alessandro Ederoclite.")
	print("")
	print("Be Excellent to Each Other.")
	print("--------------------------------------------------------------")

	OBSERVATION_MODE = input("Choose the type of observation being made (imaging or spectroscopy) = ")
	SOURCE_TYPE = input("Choose the type of source being observed (point or extended) = ")

	flux_input_type = input("Choose a type of flux input (blackbody, template, power_law, continuum or single_line_source) = ")

	if(flux_input_type == "blackbody"):
		temperature = units.K * float(input("BLACKBODY: Choose the object temperature (K) = "))
	elif(flux_input_type == "template"):
		flux_template = input ("TEMPLATE: Enter the flux template file location = ")
		redshift = (units.m/units.m) * float(input("TEMPLATE: Enter a redshift to shift template = "))
	elif(flux_input_type == "power_law"):
		reference_wavelength = units.micrometer * float(input("POWER LAW: Enter the reference wavelength = "))
		power_law_index = (units.m/units.m) * float(input("POWER LAW: Enter the power law index = "))
		reference_flux = flux_unit * float(input("POWER LAW: Enter reference flux = "))
	elif(flux_input_type == "continuum"):
		reference_flux = flux_unit * float(input("CONTINUUM: Enter reference flux = "))
	elif(flux_input_type == "single_line_source"):
		line_central_wavelength = units.micrometer * float(input("SLS: Enter line central wavelength = "))
		line_fwhm = units.micrometer * float(input("SLS: Enter line full width at half maximum = "))
		line_total_flux = flux_unit * float(input("SLS: Enter line total flux = "))

	observed_wavelength = units.micrometer * float(input("Observed at wavelength (um) = "))

	if(OBSERVATION_MODE == "imaging"):
		filter_band_width = (units.micrometer * units.bin**-1) * float(input("Enter the filter band width (um) = "))
	elif(OBSERVATION_MODE == "spectroscopy"):
		spectral_bin = units.micrometer * float(input("Enter the spectral bin (um/bin)"))

	telescope_surface = (units.meter**2) * float(input("Enter the telescope surface area (m²) = "))
	exposure_time = units.second * float(input("Enter the exposure time (s) = "))
	efficiency = (units.m/units.m) * float(input("Enter the telescope efficiency = "))

def photon_energy(wavelength_um):
	#Takes a wavelength (in um), and returns the energy of a single photon of that wavelength
	P = (h * c) / wavelength_um
	return P * (units.ph**-1)

def electrons_per_bin():

	if(OBSERVATION_MODE == "imaging"):
		delta = filter_band_width

	elif(OBSERVATION_MODE == "spectroscopy"):
		delta = spectral_bin

	if(SOURCE_TYPE == "point"):
		omega = 1 * units.sr

	elif(SOURCE_TYPE == "extended"):
		omega = solid_angle * units.sr

	if(flux_input_type == "blackbody"):
		incident_flux = blackbody_lambda(observed_wavelength, temperature)
	elif(flux_input_type == "continuum"):
		incident_flux = reference_flux

	print("CALCULATING N")
	N = (incident_flux * delta * exposure_time * efficiency * telescope_surface * omega) / photon_energy(observed_wavelength)
	return N.decompose()

user_input()
print(electrons_per_bin())

#	Affonso is still here,
#	Be excellent to each other.
# 
#   00:50, Friday, April 5th, 2019, São Paulo, Brasil, Earth.