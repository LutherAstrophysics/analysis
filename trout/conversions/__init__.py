import math

def flux_to_magnitude_4px(flux): 
    """ Converts 4px star flux data to magnitude """
    return 24.176 - (2.6148 * math.log10(flux))

def mag_4px_to_flux(mag): 
    """ Converts 4px magnitude to flux value """
    return 10** ((-(-24.176 + mag))/2.6148)
