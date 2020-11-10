#Copyright 2018-2019 Affonso Amendola
#Distributed under GPL V3 License, check the LICENSE file for more info.

#Generic Exposure Time Calculator
#GeTC
import numpy as np

from astropy.modeling.models import BlackBody
from astropy.constants import h, c
from astropy import units

VERSION = 0.04
DEBUG = False

FLUX_UNIT = units.joule * (units.second**-1) * (units.meter**-2) * (units.micrometer**-1)

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
	def __init__(self, element_name, optical_response_table_file, transmittance=False):
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
	primary_mirror_focal_length = units.mm * 9098 #mm JST/T250

	#line_central_wavelength = 0
	#line_fwhm = 0
	#line_total_flux = 0

	observed_wavelength = units.micrometer * 0.6

	filter_band_width = 0
	#spectral_bin = 0

	telescope_surface = (units.m**2) * 3.75 #m2 JST/T250
	exposure_time = (units.s) * 0

	read_out_noise = (units.electron) * 3.4 #JPAS-Pathfinder
	dark_current = (units.electron * (units.s**-1)) * 0.0008 #JPAS-Pathfinder

	number_of_exposures = 1

	sky_mag = 0
	airmass = 1

class InstrumentConfiguration:
	def __init__(self, config_file):
	#Uses a configuration file to setup all the currently installed mirrors and stuff on the telescope.
		if(DEBUG): print("\nDEBUG: Loading Instrument Configuration from file ", config_file)

		self.m_element_list = []
		with open(config_file, 'r') as f:
			for line in f:
				values = line.split()
				transmittance = (values[2]=="1")

				if(DEBUG): print("\n", values[0], values[1], transmittance)
				
				new_optical_element = OpticalElement( values[0], values[1], transmittance=transmittance)
				self.m_element_list.append( new_optical_element )

	def get_efficiency_at(self, wavelength_um):
	#Takes a value of wavelength in micrometer and returns the telescope efficiency 
	#at that wavelength, in it's current configuration.
		efficiency = 1.

		for optical_element in self.m_element_list:
			efficiency = efficiency * optical_element.get_efficiency_at(wavelength_um)

		return efficiency
		
def user_input():
	user_config = ObservationConfiguration()

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

#	user_config.telescope_surface = (units.meter**2) * float(input("Enter the telescope surface area (m²) = "))
	user_config.exposure_time = units.second * float(input("Enter the exposure time (s) = "))

	user_config.sky_mag = units.ABmag * float(input("Enter sky contribution (magAB/arcsec^2) = "))
	user_config.airmass = float(input("Enter airmass around observation = "))

	return user_config

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
			observation_config.telescope_surface * omega) / photon_energy(observation_config.observed_wavelength)	

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
	print("* surface <- ", observation_config.telescope_surface)
	print("* omega <- ", omega)
	print("/ photon energy <- ", photon_energy(observation_config.observed_wavelength))

	n_obj = (incident_flux * delta * observation_config.exposure_time * instrument_config.get_efficiency_at(observation_config.observed_wavelength) * \
			observation_config.telescope_surface * omega) / photon_energy(observation_config.observed_wavelength)

	n_obj = n_obj.decompose() * (units.electron) / (units.ph)

	signal = n_obj * observation_config.number_of_exposures

	n_sky = sky_contribution(observation_config, instrument_config) * observation_config.number_of_exposures

	print("N Object = ", n_obj)
	print("N Sky = ", n_sky)

	noise = np.sqrt(n_obj + n_sky + (observation_config.read_out_noise**2)*(units.electron**-1) + \
					observation_config.dark_current * observation_config.number_of_exposures * observation_config.exposure_time)*(units.electron**(1/2))

	return signal, noise


def main():
	print("-------------------------------------------")
	print("GeTC ver. ", VERSION)
	print("Made by Affonso Amendola.")
	print("Under orientation of Alessandro Ederoclite.")
	print("Be Excellent to Each Other.")
	print("-------------------------------------------")

	instrument_config = InstrumentConfiguration("optical_config")

	observation_config = user_input()
	#Current_config is a ObservationConfiguration type, so its members are the current config, and user_input returns a
	#new ObservationConfiguration instance with the users requested config
	signal, noise = signal_to_noise_ratio(observation_config, instrument_config)

	print("Signal = ", signal)
	print("Noise = ", noise)
	print("S/N = ", signal/noise)

main()

#	Foffonso was here,
#	Be excellent to each other.
# 
#   17:20, Wednesday, October 14th, 2020, Sao Paulo, Brasil, Earth.