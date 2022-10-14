from trout.database import query

STAR_START = 1
STAR_END = 2510

def is_valid_star(star_number: int):
    return star_number >= STAR_START and star_number <= STAR_END

def star_table_name(star_number: int):

    # Only return if valid star_number provided
    if is_valid_star(star_number):
        return f"star_{star_number}_4px"

def get_star_data(star_number : int):
    """
    Gives the stars data from the database for a particular star.
    param: star_number 
    return: tuple of 3 tuple consiting (id, magnitude, date)
    """

    table = star_table_name(star_number)

    if table:
        # Tuple used for enforcing immutabilty
        return tuple(query(f"SELECT * FROM {table}"))

