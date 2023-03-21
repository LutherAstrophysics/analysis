from datetime import date
from functools import cache
from typing import Iterable

from trout.stars import get_star


@cache
def get_nights_in_a_year(year: int, is_primary: bool = True) -> Iterable[date]:
    """
    Returns the list of all night dates for a given `year`
    Note that we get the list of dates by just looking at the nights
    on which star 1 had data.
    """
    star_one = get_star(1, is_primary)
    # Select data for the given year
    # Note that we're not excluding bad nights and zero values
    star_one.select(
        f"date >= '{year}-01-01' and date< '{year + 1}-01-01'",
        exclude_bad_nights=False,
        exclude_zeros=False)
    return star_one.get_selected_dates_column()
