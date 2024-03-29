import re

# If we had added m23 as a dependency we wouldn't need to add this file module
# as it's already implemented in the m23 library. But m23 library is too big and
# perhaps unnecessary to add as a dependency.


def line_str_contains_numbers_and_non_alphabets(line_str: str) -> bool:
    """
    Check if the `line_str` contains at least one digit and non alphabetical
    characters
    """
    return re.search(r"\d+", line_str) and not re.search("[a-zA-Z]", line_str)
