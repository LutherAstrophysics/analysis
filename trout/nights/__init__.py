from trout.database import query

def bad_nights(limit:int=0):
    """
    Get the list of bad nights from the database.

    param limit(optional): number of results to limit to
    return: List of 2 tuple (id, date)
    """
    if limit > 0: 
        return query(f"SELECT * FROM bad_nights LIMIT {limit}")

    # Tuple used for enforcing immutabilty
    return tuple(query(f"SELECT * FROM bad_nights"))
