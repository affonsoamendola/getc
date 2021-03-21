#!/bin/python3
#Copyright 2018-2019 Affonso Amendola
#Distributed under GPL V3 License, check the LICENSE file for more info.

#Generic Exposure Time Calculator
#GeTC
import numpy as np
import sys

from astropy.modeling.models import BlackBody
from astropy.constants import h, c
from astropy import units

VERSION = 0.06
DEBUG = False

FLUX_UNIT = units.joule * (units.second**-1) * (units.meter**-2) * (units.micrometer**-1)

CONFIG_FILE = "optical_config"

FILTERS = {
	"JPAS":
	{
		"gSDSS":"optics/filters/J-PAS/OAJ_JPAS.gSDSS.dat",
		"iSDSS":"optics/filters/J-PAS/OAJ_JPAS.iSDSS.dat",
		"J0378":"optics/filters/J-PAS/OAJ_JPAS.J0378.dat",
		"J0390":"optics/filters/J-PAS/OAJ_JPAS.J0390.dat",
		"J0400":"optics/filters/J-PAS/OAJ_JPAS.J0400.dat",
		"J0410":"optics/filters/J-PAS/OAJ_JPAS.J0410.dat",
		"J0420":"optics/filters/J-PAS/OAJ_JPAS.J0420.dat",
		"J0430":"optics/filters/J-PAS/OAJ_JPAS.J0430.dat",
		"J0440":"optics/filters/J-PAS/OAJ_JPAS.J0440.dat",
		"J0450":"optics/filters/J-PAS/OAJ_JPAS.J0450.dat",
		"J0460":"optics/filters/J-PAS/OAJ_JPAS.J0460.dat",
		"J0470":"optics/filters/J-PAS/OAJ_JPAS.J0470.dat",
		"J0480":"optics/filters/J-PAS/OAJ_JPAS.J0480.dat",
		"J0490":"optics/filters/J-PAS/OAJ_JPAS.J0490.dat",
		"J0500":"optics/filters/J-PAS/OAJ_JPAS.J0500.dat",
		"J0510":"optics/filters/J-PAS/OAJ_JPAS.J0510.dat",
		"J0520":"optics/filters/J-PAS/OAJ_JPAS.J0520.dat",
		"J0530":"optics/filters/J-PAS/OAJ_JPAS.J0530.dat",
		"J0540":"optics/filters/J-PAS/OAJ_JPAS.J0540.dat",
		"J0550":"optics/filters/J-PAS/OAJ_JPAS.J0550.dat",
		"J0560":"optics/filters/J-PAS/OAJ_JPAS.J0560.dat",
		"J0570":"optics/filters/J-PAS/OAJ_JPAS.J0570.dat",
		"J0580":"optics/filters/J-PAS/OAJ_JPAS.J0580.dat",
		"J0590":"optics/filters/J-PAS/OAJ_JPAS.J0590.dat",
		"J0600":"optics/filters/J-PAS/OAJ_JPAS.J0600.dat",
		"J0610":"optics/filters/J-PAS/OAJ_JPAS.J0610.dat",
		"J0620":"optics/filters/J-PAS/OAJ_JPAS.J0620.dat",
		"J0630":"optics/filters/J-PAS/OAJ_JPAS.J0630.dat",
		"J0640":"optics/filters/J-PAS/OAJ_JPAS.J0640.dat",
		"J0650":"optics/filters/J-PAS/OAJ_JPAS.J0650.dat",
		"J0660":"optics/filters/J-PAS/OAJ_JPAS.J0660.dat",
		"J0670":"optics/filters/J-PAS/OAJ_JPAS.J0670.dat",
		"J0680":"optics/filters/J-PAS/OAJ_JPAS.J0680.dat",
		"J0690":"optics/filters/J-PAS/OAJ_JPAS.J0690.dat",
		"J0700":"optics/filters/J-PAS/OAJ_JPAS.J0700.dat",
		"J0710":"optics/filters/J-PAS/OAJ_JPAS.J0710.dat",
		"J0720":"optics/filters/J-PAS/OAJ_JPAS.J0720.dat",
		"J0730":"optics/filters/J-PAS/OAJ_JPAS.J0730.dat",
		"J0740":"optics/filters/J-PAS/OAJ_JPAS.J0740.dat",
		"J0750":"optics/filters/J-PAS/OAJ_JPAS.J0750.dat",
		"J0760":"optics/filters/J-PAS/OAJ_JPAS.J0760.dat",
		"J0770":"optics/filters/J-PAS/OAJ_JPAS.J0770.dat",
		"J0780":"optics/filters/J-PAS/OAJ_JPAS.J0780.dat",
		"J0790":"optics/filters/J-PAS/OAJ_JPAS.J0790.dat",
		"J0800":"optics/filters/J-PAS/OAJ_JPAS.J0800.dat",
		"J0810":"optics/filters/J-PAS/OAJ_JPAS.J0810.dat",
		"J0820":"optics/filters/J-PAS/OAJ_JPAS.J0820.dat",
		"J0830":"optics/filters/J-PAS/OAJ_JPAS.J0830.dat",
		"J0840":"optics/filters/J-PAS/OAJ_JPAS.J0840.dat",
		"J0850":"optics/filters/J-PAS/OAJ_JPAS.J0850.dat",
		"J0860":"optics/filters/J-PAS/OAJ_JPAS.J0860.dat",
		"J0870":"optics/filters/J-PAS/OAJ_JPAS.J0870.dat",
		"J0880":"optics/filters/J-PAS/OAJ_JPAS.J0880.dat",
		"J0890":"optics/filters/J-PAS/OAJ_JPAS.J0890.dat",
		"J0900":"optics/filters/J-PAS/OAJ_JPAS.J0900.dat",
		"J0910":"optics/filters/J-PAS/OAJ_JPAS.J0910.dat",
		"J1007":"optics/filters/J-PAS/OAJ_JPAS.J1007.dat",
		"rSDSS":"optics/filters/J-PAS/OAJ_JPAS.rSDSS.dat",
		"u":"optics/filters/J-PAS/OAJ_JPAS.u.dat",
		"uJava":"optics/filters/J-PAS/OAJ_JPAS.uJava.dat"
	}
}

#class TemplateSpectra:
	#	def __init__(self, file_name):
	#		self.m_file_name = file_name
	#		self.m_angstrom = []
	#		self.m_flux = []
	#
	#		with open(self.m_file_name, 'r') as f:
	#			for line in f:
	#				if(line[0] != '#'):
	#					#Ignore Comments
	#					values = line.split()
	#
	#					if(DEBUG): print(values[0], values[1])
	#
	#					self.m_angstrom.append(float(values[0]))
	#					self.m_flux.append(float(values[1])) 
	#
	#	def get_flux_at(self, wavelength_um):
	#
	#		wavelength_ang = wavelength_um * float(units.micrometer.to(units.angstrom))
	#		flux = np.interp(wavelength_ang, self.m_angstrom, self.m_flux)
	#
	#		if(DEBUG): print("DEBUG: Template Spectra flux at : ", wavelength_um, ", is : ", flux)
	#
	#		return flux

class OpticalElement:
	def __init__(self, element_name, optical_response_table_file, transmittance=True):
		self.m_name = element_name
		self.m_response_angstrom = []
		self.m_response_efficiency = []

		if(DEBUG): print("DEBUG: New Optical Element ", self.m_name)

		#Opens optical_response_table_file
		with open(optical_response_table_file, 'r') as f:
			for line in f:
				if(line[0] != '#'):
					#Ignore comments
					values = line.split()

					if(DEBUG): print(values[0], values[1])

					self.m_response_angstrom.append(float(values[0]) * units.angstrom)
					#First entry in the file lists the wavelength
					#TODO: More formats, different units.	

					#Iftransmittance is True, just add the value as is.
					if(transmittance == True):
						self.m_response_efficiency.append(float(values[1])) 
					else:
						#Else, transform absorbance value in transmittance
						self.m_response_efficiency.append(1.0 - float(values[1])) 

	def get_efficiency_at(self, wavelength_um):

		wavelength_ang = wavelength_um.to(units.angstrom)
		efficiency = np.interp(wavelength_ang, self.m_response_angstrom, self.m_response_efficiency)

		if(DEBUG): print("DEBUG: Optical Element ", self.m_name, " efficiency at ", wavelength_um, ", is :", efficiency)

		return efficiency

class ObservationConfiguration:
	SOURCE_TYPE = "point"
	OBSERVATION_MODE = "imaging"

	#flux_input_type = "a"

	#temperature = units.K * 5000

	#flux_template = ""
	#redshift = 0	

	object_magnitude = 0

	#reference_wavelength = 0
	#power_law_index = 0
	#reference_flux = 0

	#primary_mirror_diameter = 0

	#line_central_wavelength = 0
	#line_fwhm = 0
	#line_total_flux = 0

	observed_wavelength = units.micrometer * 0.6

	filter_band_width = 0
	#spectral_bin = 0

	exposure_time = (units.s) * 0

	number_of_exposures = 1

	sky_mag = 0
	airmass = 1

def parse_optical_config_file(config_file, instrument_config):
	for line in config_file:
		if(line[0] == '#'):
			continue

		values = line.split()
		
		if(len(values) == 0):
			continue

		if(values[0] == "filter_list"):
			instrument_config.filter_list = values[1]
			if(DEBUG): print("DEBUG: Filter List = ", instrument_config.filter_list)
			continue

		if(values[0] == "primary_mirror_focal_length"):
			instrument_config.primary_mirror_focal_length = float(values[1]) * units.mm
			if(DEBUG): print("DEBUG: Primary focal length = ", instrument_config.primary_mirror_focal_length)
			continue

		if(values[0] == "effective_collecting_area"):
			instrument_config.effective_collecting_area = float(values[1]) * (units.m**2)
			if(DEBUG): print("DEBUG: Effective Collecting Area = ", instrument_config.effective_collecting_area)
			continue

		if(values[0] == "read_out_noise"):
			instrument_config.read_out_noise = float(values[1]) * (units.electron)
			if(DEBUG): print("DEBUG: Read out noise = ", instrument_config.read_out_noise)
			continue	

		if(values[0] == "dark_current"):
			instrument_config.dark_current = float(values[1]) * units.electron * (units.second**-1)
			if(DEBUG): print("DEBUG: Dark current = ", instrument_config.dark_current)
			continue

		new_optical_element = OpticalElement( values[0], values[1])
		instrument_config.m_element_list.append( new_optical_element )

class InstrumentConfiguration:
	filter_list = ""
	primary_mirror_focal_length = 0.0
	effective_collecting_area = 0.0

	read_out_noise = 0.0
	dark_current = 0.0

	def __init__(self, config_file):
	#Uses a configuration file to setup all the currently installed mirrors and stuff on the telescope.
		if(DEBUG): print("\nDEBUG: Loading Instrument Configuration from file ", config_file)

		self.m_element_list = []
		with open(config_file, 'r') as f:
			parse_optical_config_file(f, self)

	def add_filter(self, filter_name, filter_location):
		new_optical_element = OpticalElement( filter_name, filter_location)
		self.m_element_list.append( new_optical_element )

	def get_efficiency_at(self, wavelength_um):
	#Takes a value of wavelength in micrometer and returns the telescope efficiency 
	#at that wavelength, in it's current configuration.
		efficiency = 1.

		for optical_element in self.m_element_list:
			efficiency = efficiency * optical_element.get_efficiency_at(wavelength_um)

		return efficiency
		
def user_input():

	if(CONFIG_FILE == "optical_config"):
		print("Using default configuration file.")
	else:
		print("Using \"" + CONFIG_FILE + "\" as the configuration file.")

	instrument_config = InstrumentConfiguration(CONFIG_FILE)
	user_config = ObservationConfiguration()

	filter_input = False

	while (filter_input == False):
		filter_name = input("Enter installed filter (Or type \"list\" to list all available filters) = ")

		if(filter_name == "list"):
			for key in FILTERS[instrument_config.filter_list]:
				print(key)

		filter_location = FILTERS[instrument_config.filter_list].get(filter_name, "")

		if(filter_location != ""):
			instrument_config.add_filter(filter_name, filter_location)
			filter_input = True


#	user_config.OBSERVATION_MODE = input("Choose the type of observation being made (imaging or spectroscopy) = ")
#	user_config.SOURCE_TYPE = input("Choose the type of source being observed (point or extended) = ")

	user_config.object_magnitude = units.ABmag * float(input("Enter object apparent magnitude = "))

#	user_config.primary_mirror_focal_length = units.mm * input("Enter primary mirror focal length (in mm) = ")

#	user_config.flux_input_type = input("Choose a type of flux input (blackbody, template, power_law, continuum or single_line_source) = ")

#	if(user_config.flux_input_type == "blackbody"):

#		user_config.temperature = units.K * float(input("BLACKBODY: Choose the object temperature (K) = "))

#	elif(user_config.flux_input_type == "template"):

#		user_config.flux_template_file = input ("TEMPLATE: Enter the flux template file location = ")
#		user_config.redshift = (units.m/units.m) * float(input("TEMPLATE: Enter a redshift to shift template = "))
#		user_config.flux_template = TemplateSpectra(user_config.flux_template_file)
	
#	elif(user_config.flux_input_type == "power_law"):

#		user_config.reference_wavelength = units.micrometer * float(input("POWER LAW: Enter the reference wavelength = "))
#		user_config.power_law_index = (units.m/units.m) * float(input("POWER LAW: Enter the power law index = "))
#		user_config.reference_flux = FLUX_UNIT * float(input("POWER LAW: Enter reference flux = "))
	
#	elif(user_config.flux_input_type == "continuum"):
		
#		user_config.reference_flux = FLUX_UNIT * float(input("CONTINUUM: Enter reference flux = "))
	
#	elif(user_config.flux_input_type == "single_line_source"):
		
#		user_config.line_central_wavelength = units.micrometer * float(input("SLS: Enter line central wavelength = "))
#		user_config.line_fwhm = units.micrometer * float(input("SLS: Enter line full width at half maximum = "))
#		user_config.line_total_flux = user_config.FLUX_UNIT * float(input("SLS: Enter line total flux = "))

	user_config.observed_wavelength = units.micrometer * float(input("Observed at wavelength (um) = "))

	if(user_config.OBSERVATION_MODE == "imaging"):
		user_config.filter_band_width = (units.micrometer) * float(input("Enter the filter band width (um) = "))
	elif(OBSERVATION_MODE == "spectroscopy"):
		user_config.spectral_bin = units.micrometer * float(input("Enter the spectral bin (um/bin)"))

#	user_config.effective_collecting_area = (units.meter**2) * float(input("Enter the telescope surface area (m²) = "))
	user_config.exposure_time = units.second * float(input("Enter the exposure time (s) = "))
	user_config.number_of_exposures = int(input("Enter the number of exposures = "))

	user_config.sky_mag = units.ABmag * float(input("Enter sky contribution (magAB/arcsec^2) = "))
	user_config.airmass = float(input("Enter airmass around observation = "))

	return user_config, instrument_config

def photon_energy(wavelength_um):
	#Takes a wavelength (in um), and returns the energy of a single photon of that wavelength
	P = (h * c) / wavelength_um
	return (P * (units.ph**-1)).decompose()

def sky_contribution(observation_config, instrument_config):
	sky_flux = observation_config.sky_mag.to(units.erg * (units.s**-1) * (units.cm**-2) * (units.Hz**-1))
	sky_flux = sky_flux * (c / (observation_config.observed_wavelength**2))

	if(observation_config.OBSERVATION_MODE == "imaging"):
		delta = observation_config.filter_band_width

	elif(observation_config.OBSERVATION_MODE == "spectroscopy"):
		delta = observation_config.spectral_bin

	omega = 1

	n_sky = (sky_flux * delta * observation_config.exposure_time * instrument_config.get_efficiency_at(observation_config.observed_wavelength) * \
			instrument_config.effective_collecting_area * omega) / photon_energy(observation_config.observed_wavelength)	

	return n_sky.decompose() * (units.electron) / (units.ph)

def signal_to_noise_ratio(observation_config, instrument_config):
	
	if(observation_config.OBSERVATION_MODE == "imaging"):
		delta = observation_config.filter_band_width

	elif(observation_config.OBSERVATION_MODE == "spectroscopy"):
		delta = observation_config.spectral_bin

	omega = 1

	#if(observation_config.SOURCE_TYPE == "point"):
		#omega = (206265 * 15 * units.micrometer)/(1000 * observation_config.primary_mirror_focal_length) * (units.arcsec**2) * (units.pix **-1) 

	#elif(observation_config.SOURCE_TYPE == "extended"):
		#omega = observation_config.solid_angle * units.sr

#	if(observation_config.flux_input_type == "blackbody"):
#		blackbody_model = BlackBody(temperature=observation_config.temperature)
#		incident_flux = blackbody_model(observation_config.observed_wavelength)
#	elif(observation_config.flux_input_type == "continuum"):
#		incident_flux = observation_config.reference_flux
#	elif(observation_config.flux_input_type == "template"):
#		incident_flux = observation_config.flux_template.get_flux_at(observation_config.observed_wavelength)

	incident_flux = observation_config.object_magnitude.to(units.erg * (units.s**-1) * (units.cm**-2) * (units.Hz**-1))
	incident_flux = incident_flux * (c / (observation_config.observed_wavelength**2))

	print("incident_flux = ", incident_flux)
	print("* delta <- ", delta)
	print("* exposure_time <- ", observation_config.exposure_time)
	print("* efficiency <- ", instrument_config.get_efficiency_at(observation_config.observed_wavelength))
	print("* surface <- ", instrument_config.effective_collecting_area)
	print("* omega <- ", omega)
	print("/ photon energy <- ", photon_energy(observation_config.observed_wavelength))

	n_obj = (incident_flux * delta * observation_config.exposure_time * instrument_config.get_efficiency_at(observation_config.observed_wavelength) * \
			instrument_config.effective_collecting_area * omega) / photon_energy(observation_config.observed_wavelength)

	n_obj = n_obj.decompose() * (units.electron) / (units.ph)

	signal = n_obj * observation_config.number_of_exposures

	n_sky = sky_contribution(observation_config, instrument_config) * observation_config.number_of_exposures

	print("N Object = ", n_obj)
	print("N Sky = ", n_sky)

	noise = np.sqrt(n_obj + n_sky + (instrument_config.read_out_noise**2)*(units.electron**-1) + \
					instrument_config.dark_current * observation_config.number_of_exposures * observation_config.exposure_time)*(units.electron**(1/2))

	return signal, noise


def main():
	print("-------------------------------------------")
	print("GeTC ver. ", VERSION)
	print("Made by Affonso Amendola.")
	print("Under orientation of Alessandro Ederoclite.")
	print("Be Excellent to Each Other.")
	print("-------------------------------------------")

	parse_command_line()

	observation_config, instrument_config = user_input()

	#Current_config is a ObservationConfiguration type, so its members are the current config, and user_input returns a
	#new ObservationConfiguration instance with the users requested config
	signal, noise = signal_to_noise_ratio(observation_config, instrument_config)

	print("Signal = ", signal)
	print("Noise = ", noise)
	print("S/N = ", signal/noise)

def parse_command_line():

	args = sys.argv[1:]


	while(len(args) >= 1):
		arg = args.pop()

		if(arg == "-h" or arg == "--h" or arg == "-help" or arg == "--help" or arg == "-?"):
			print_help()
			exit()

		if(arg == "-d" or arg == "--d" or arg == "--debug"):
			global DEBUG
			DEBUG = True
			continue

		if(arg.startswith("-") or arg.startswith("--")):
			print ("Unknown options, type --help for help")
			exit()

		global CONFIG_FILE
		CONFIG_FILE = arg



def print_help():
	print("Usage: ./gmt_etc.py [-h] [-d] [config_file]")
	print("Options:")
	print(" -h, --help, -? 	Prints this help message.")
	print(" -d, --debug 		Enables debug messages.")
	print("")
	print(" config_file 		The name of the config file to use,")
	print("                 	will default to \"optical_config\"")

main()

#	Foffonso was here,
#	Be excellent to each other.
# 
#   17:20, Wednesday, October 14th, 2020, Sao Paulo, Brasil, Earth.