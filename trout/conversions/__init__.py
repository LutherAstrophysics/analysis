import math

def flux_to_magnitude_4px(flux): 
    """ Converts 4px star flux data to magnitude """
    value = 24.176 - (2.6148 * math.log10(flux))
    return value
