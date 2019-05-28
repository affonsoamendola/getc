#Copyright 2018 Affonso Amendola
#Distributed under GPL V3 License, check the LICENSE file for more info.

#GMT Exposure Time Calculator

import numpy as np

from astropy.modeling.blackbody import blackbody_lambda
from astropy.constants import h, c
from astropy import units

VERSION = 0.01

FLUX_UNIT = units.joule * (units.second**-1) * (units.meter**-2) * (units.micrometer**-1) * (units.sr**-1)

class OpticalElement:
	def __init__(self, element_name, optical_response_table_file):
		self.m_name = ""
		self.m_response_angstrom = []
		self.m_response_efficiency = []

		#Opens optical_response_table_file
		with open(optical_response_table_file, 'r') as f:
			for line in f:
				if(line[0] != '#'):
					#Ignore Comments comments
					values = line.split()
					self.m_response_angstrom.append(float(values[0]))
					self.m_response_efficiency.append(float(values[1])) 

	def get_efficiency_at(self, wavelength_um):

		wavelength_ang = wavelength_um * float(units.micrometer.to(units.angstrom))
		efficiency = np.interp(wavelength_ang, self.m_response_angstrom, self.m_response_efficiency)

		return efficiency

class ObservationConfiguration:
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

class InstrumentConfiguration:
	def __init__(self, config_file):
	#Uses a configuration file to setup all the currently installed mirrors and stuff on the telescope.
		self.m_element_list = []
		with open(config_file, 'r') as f:
			for line in f:
				values = line.split()
				new_optical_element = OpticalElement( values[0], values[1] )
				self.m_element_list.append( new_optical_element )

	def get_efficiency_at(self, wavelength_um):
	#Takes a value of wavelength in micrometer and returns the telescope efficiency 
	#at that wavelength, in it's current configuration.
		efficiency = 1.

		for optical_element in self.m_element_list:
			efficiency = efficiency * optical_element.get_efficiency_at(wavelength_um)

		return (units.m/units.m) * efficiency
		
def user_input():
	user_config = ObservationConfiguration()

	user_config.OBSERVATION_MODE = input("Choose the type of observation being made (imaging or spectroscopy) = ")
	user_config.SOURCE_TYPE = input("Choose the type of source being observed (point or extended) = ")

	user_config.flux_input_type = input("Choose a type of flux input (blackbody, template, power_law, continuum or single_line_source) = ")

	if(user_config.flux_input_type == "blackbody"):

		user_config.temperature = units.K * float(input("BLACKBODY: Choose the object temperature (K) = "))

	elif(user_config.flux_input_type == "template"):

		user_config.flux_template = input ("TEMPLATE: Enter the flux template file location = ")
		user_config.redshift = (units.m/units.m) * float(input("TEMPLATE: Enter a redshift to shift template = "))
	
	elif(user_config.flux_input_type == "power_law"):

		user_config.reference_wavelength = units.micrometer * float(input("POWER LAW: Enter the reference wavelength = "))
		user_config.power_law_index = (units.m/units.m) * float(input("POWER LAW: Enter the power law index = "))
		user_config.reference_flux = FLUX_UNIT * float(input("POWER LAW: Enter reference flux = "))
	
	elif(user_config.flux_input_type == "continuum"):
		
		user_config.reference_flux = FLUX_UNIT * float(input("CONTINUUM: Enter reference flux = "))
	
	elif(user_config.flux_input_type == "single_line_source"):
		
		user_config.line_central_wavelength = units.micrometer * float(input("SLS: Enter line central wavelength = "))
		user_config.line_fwhm = units.micrometer * float(input("SLS: Enter line full width at half maximum = "))
		user_config.line_total_flux = user_config.FLUX_UNIT * float(input("SLS: Enter line total flux = "))

	user_config.observed_wavelength = units.micrometer * float(input("Observed at wavelength (um) = "))

	if(user_config.OBSERVATION_MODE == "imaging"):
		user_config.filter_band_width = (units.micrometer * units.bin**-1) * float(input("Enter the filter band width (um) = "))
	elif(OBSERVATION_MODE == "spectroscopy"):
		user_config.spectral_bin = units.micrometer * float(input("Enter the spectral bin (um/bin)"))

	user_config.telescope_surface = (units.meter**2) * float(input("Enter the telescope surface area (m²) = "))
	user_config.exposure_time = units.second * float(input("Enter the exposure time (s) = "))

	return user_config

def photon_energy(wavelength_um):
	#Takes a wavelength (in um), and returns the energy of a single photon of that wavelength
	P = (h * c) / wavelength_um
	return P * (units.ph**-1)

def electrons_per_bin(observation_config, instrument_config):
	
	if(observation_config.OBSERVATION_MODE == "imaging"):
		delta = observation_config.filter_band_width

	elif(observation_config.OBSERVATION_MODE == "spectroscopy"):
		delta = observation_config.spectral_bin

	if(observation_config.SOURCE_TYPE == "point"):
		omega = 1 * units.sr

	elif(observation_config.SOURCE_TYPE == "extended"):
		omega = observation_config.solid_angle * units.sr

	if(observation_config.flux_input_type == "blackbody"):
		incident_flux = blackbody_lambda(observation_config.observed_wavelength, observation_config.temperature)
	elif(observation_config.flux_input_type == "continuum"):
		incident_flux = observation_config.reference_flux

	print("CALCULATING N")
	N = (incident_flux * delta * observation_config.exposure_time * instrument_config.get_efficiency_at(observation_config.observed_wavelength) * \
		observation_config.telescope_surface * omega) / photon_energy(observation_config.observed_wavelength)
	return N.decompose()

def main():
	print("--------------------------------------------------------------")
	print("GMT-ETC ver. ", VERSION)
	print("Made by Affonso Amendola, under request and orientation of Alessandro Ederoclite.")
	print("")
	print("Be Excellent to Each Other.")
	print("--------------------------------------------------------------")

	instrument_config = InstrumentConfiguration("optical_config")

	observation_config = user_input()
	#Current_config is a ObservationConfiguration type, so its members are the current config, and user_input returns a
	#new ObservationConfiguration instance with the users requested config
	print("This is an aproximation of how many counts per bin:")
	print(electrons_per_bin(observation_config, instrument_config))

main()

#	Affonso is still here,
#	Be excellent to each other.
# 
#   00:50, Friday, April 5th, 2019, São Paulo, Brasil, Earth.