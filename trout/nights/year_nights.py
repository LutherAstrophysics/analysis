from datetime import date
from functools import cache
from typing import Iterable
from trout.stars import get_star


@cache
def get_nights_in_a_year(year: int) -> Iterable[date]:
    """
    Returns the list of all night dates for a given `year`
    Note that we get the list of dates by just looking at the nights
    on which star 1 had data.
    """
    star_one = get_star(1)
    # Select data for the given year
    star_one.select(f"date >= '{year}-01-01' and date< '{year + 1}-01-01'")
    return star_one.get_selected_dates_column()
