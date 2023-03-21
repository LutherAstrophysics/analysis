from functools import cache

from trout.database import query


@cache
def bad_nights(limit: int = 0, is_primary: bool = True):
    """
    Get the list of bad nights from the database.
    Note that this function is cached which means that if you have recently made
    changes to the list of bad_nights, then you might have to be careful.

    param limit(optional): number of results to limit to. Defaults to no limit.
    return: List of 2 tuple (id, date)
    """
    if limit > 0:
        if is_primary:
            return query(f"SELECT * FROM bad_nights LIMIT {limit}")
        else:
            return query(f"SELECT * FROM bad_nights_exp LIMIT {limit}")

    # Tuple used for enforcing immutability
    if is_primary:
        return tuple(query("SELECT * FROM bad_nights"))
    else:
        return tuple(query("SELECT * FROM bad_nights_exp"))
