from functools import cache
from typing import Union

from trout.database import query


@cache
def bad_nights(limit: int = 0, is_primary: bool = True, year: Union[None, int] = None):
    """
    Get the list of bad nights from the database.
    Note that this function is cached which means that if you have recently made
    changes to the list of bad_nights, then you might have to be careful.

    @param limit(optional): number of results to limit to. Defaults to no limit.
    @param: is_primary (optional): whether to use primary or secondary database.
    @param: year (optional): specify year to get results for a particular year
    return: List of 2 tuple (id, date)
    """
    if limit <= 0:
        limit = "ALL"

    table_name = "bad_nights" if is_primary else "bad_nights_exp"

    if year:
        return query(
            f"SELECT * FROM {table_name} where date < '{year + 1}-01-01' and date >= '{year}-01-01' ORDER BY date LIMIT {limit} "
        )
    else:
        return query(f"SELECT * FROM {table_name}  ORDER BY date LIMIT {limit} ")
