import re


def line_str_contains_numbers_and_non_alphabets(line_str: str) -> bool:
    """
    Check if the `line_str` contains at least one digit and non alphabetical
    characters
    """
    return re.search(r"\d+", line_str) and not re.search("[a-zA-Z]", line_str)
