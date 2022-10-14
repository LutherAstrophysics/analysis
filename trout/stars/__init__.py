from .star import Star
from .utils import get_star_data, is_valid_star, STAR_START, STAR_END

def get_star(star_number : int) -> Star:
    """
    Creates and returns a Star object if the star_number is valid
    """
    if is_valid_star(star_number):
        return Star(star_number)

__all__ = [
        'STAR_START', 
        'STAR_END', 
        'get_star_data',
        'get_star'
        ]
