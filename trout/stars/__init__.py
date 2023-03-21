from .star import Star
from .utils import STAR_END, STAR_START, get_star_data, is_valid_star


def get_star(star_number: int, is_primary: bool = True) -> Star:
    """
    Creates and returns a Star object if the star_number is valid
    """
    if is_valid_star(star_number):
        return Star(star_number, is_primary)


__all__ = ["STAR_START", "STAR_END", "get_star_data", "get_star"]
