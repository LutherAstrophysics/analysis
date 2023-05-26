from functools import cache

from trout.color import get_color
from trout.exceptions import UnknownStarBandException
from trout.stars.utils import STAR_END, STAR_START


class InternightBands:
    COLOR_BAND_1 = "COLOR_BAND_1"
    COLOR_BAND_2 = "COLOR_BAND_2"
    COLOR_BAND_3 = "COLOR_BAND_3"
    SPECIAL_STARS = "SPECIAL_STARS"
    BRIGHTNESS_BAND = "BRIGHTNESS_BAND"


_SPECIAL_STARS = [
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


def _is_special_band_star(star: int) -> bool:
    return star in _SPECIAL_STARS


def _is_color_band_1(star: int, c: float) -> bool:
    return c > 0.135 and c <= 0.455 and not _is_special_band_star(star)


def _is_color_band_2(star: int, c: float) -> bool:
    return c > 0.455 and c <= 1.063 and not _is_special_band_star(star)


def _is_color_band_3(star: int, c: float) -> bool:
    return c > 1.063 and c <= 7 and not _is_special_band_star(star)


def _is_brightness_band(star: int, c: float) -> bool:
    return not (
        _is_special_band_star(star)
        or _is_color_band_1(star, c)
        or _is_color_band_2(star, c)
        or _is_color_band_3(star, c)
    )


@cache
def bands():
    """
    Returns the list of stars in respective bands as used in internight
    normalization
    """
    all_stars = range(STAR_START, STAR_END + 1)
    non_special_stars = list(set(all_stars) - set(_SPECIAL_STARS))

    color_band_1 = []
    color_band_2 = []
    color_band_3 = []
    brightness_band = []

    to_return = {
        InternightBands.COLOR_BAND_1: color_band_1,
        InternightBands.COLOR_BAND_2: color_band_2,
        InternightBands.COLOR_BAND_3: color_band_3,
        InternightBands.SPECIAL_STARS: _SPECIAL_STARS,
        InternightBands.BRIGHTNESS_BAND: brightness_band,
    }
    for s in non_special_stars:
        to_return[get_band(s)].append(s)

    return to_return


@cache
def get_band(star_no):
    """
    Return the internight normalization band for the star
    """
    c = get_color(star_no)

    # If color data is present
    if c:
        if _is_special_band_star(star_no):
            return InternightBands.SPECIAL_STARS
        elif _is_color_band_1(star_no, c):
            return InternightBands.COLOR_BAND_1
        elif _is_color_band_2(star_no, c):
            return InternightBands.COLOR_BAND_2
        elif _is_color_band_3(star_no, c):
            return InternightBands.COLOR_BAND_3
        elif _is_brightness_band(star_no, c):
            return InternightBands.BRIGHTNESS_BAND
        else:
            raise UnknownStarBandException
    # No color data
    elif _is_special_band_star(star_no):
        return InternightBands.SPECIAL_STARS
    else:
        return InternightBands.BRIGHTNESS_BAND
