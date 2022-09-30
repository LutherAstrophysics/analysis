from trout.database import connect

STAR_START = 1
STAR_END = 2510


def is_valid_star(star_number: int):
    return star_number >= STAR_START and star_number <= STAR_END


def star_table_name(star_number: int):

    # Only return if valid star_number provided
    if is_valid_star(star_number):
        return f"star_{star_number}_4px"


def get_star_data(star_number):
    """
    Gives the stars data from the database for a particular star.
    param: star_number 
    return: array of 3 tuple consiting (id, magnitude, date)
    """

    def inner(curs):
        table = star_table_name(star_number)

        # If the data is valid
        if table:
            curs.execute(f"SELECT * FROM {table}")
            return curs.fetchall()

    return connect(inner)
