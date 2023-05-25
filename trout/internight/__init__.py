from functools import cache

from trout.color import get_color
from trout.stars.utils import STAR_END, STAR_START


class InternightBands:
    COLOR_BAND_1 = "COLOR_BAND_1"
    COLOR_BAND_2 = "COLOR_BAND_2"
    COLOR_BAND_3 = "COLOR_BAND_3"
    SPECIAL_STARS = "SPECIAL_STARS"
    BRIGHTNESS_BAND = "BRIGHTNESS_BAND"


@cache
def bands():
    """
    Returns the list of stars in respective bands as used in internight
    normalization
    """
    all_stars = range(STAR_START, STAR_END + 1)
    special_stars = [
        814,
        1223,
        1654,
        1702,
        1716,
        1843,
        2437,
        2509,
        2510,
    ]
    non_special_stars = filter(lambda x: x not in special_stars, all_stars)

    color_band_1 = []
    color_band_2 = []
    color_band_3 = []

    brightness_band = []

    for s in non_special_stars:
        c = get_color(s)
        # Verify color isn't none (color for some stars is absent thus are in
        # brightness band)
        if c:
            # Color band stars
            if c > 0.135 and c <= 0.455:
                color_band_1.append(s)
            elif c > 0.455 and c <= 1.063:
                color_band_2.append(s)
            elif c > 1.063 and c <= 7:
                color_band_3.append(s)
            else:
                brightness_band.append(s)
        else:
            brightness_band.append(s)

    return {
        InternightBands.COLOR_BAND_1: color_band_1,
        InternightBands.COLOR_BAND_2: color_band_2,
        InternightBands.COLOR_BAND_3: color_band_3,
        InternightBands.SPECIAL_STARS: special_stars,
        InternightBands.BRIGHTNESS_BAND: brightness_band,
    }


@cache
def get_band(star_no):
    """
    Return the internight normalization band for the star
    """
    b = bands()
    for k, v in b.items():
        if star_no in v:
            return k
    return None
