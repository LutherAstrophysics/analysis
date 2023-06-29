import re
from datetime import date
from functools import total_ordering

import pandas as pd


@total_ordering
class FluxLogCombined:
    file_name_re = re.compile(r"(\d{2}-\d{2}-\d{2})_m23_(\d+\.\d*)-(\d{1,4})_flux\.txt")

    @classmethod
    def extract_image_number(cls, name):
        return int(cls.file_name_re.match(name)[3])

    @classmethod
    def get_radius_folder_name(cls, radius: int) -> str:
        """
        Returns the folder name to use for a given radius pixel of extraction
        """
        radii = {
            1: "One",
            2: "Two",
            3: "Three",
            4: "Four",
            5: "Five",
            6: "Six",
            7: "Seven",
            8: "Eight",
            9: "Nine",
        }
        if result := radii.get(radius):
            return f"{result} Pixel Radius"
        else:
            return f"{radius} Pixel Radius"

    def __new__(cls, night_date: date, number: int, radius: int):
        """
        Ensures each fluxlog combined instance is a singleton.
        """
        if not hasattr(cls, "files"):
            cls.files = {}
        year, month, day = night_date.year, night_date.month, night_date.day
        assert (type(year), type(month), type(day)) == (int,) * 3
        assert (type(number)) == int
        assert (type(radius)) == int
        identifier = (year, month, day, number, radius)
        if not cls.files.get(identifier):
            cls.files[identifier] = super(FluxLogCombined, cls).__new__(cls)
        return cls.files[identifier]

    def __init__(self, night_date: date, star_number: int, radius: int):
        from .night import Night
        self._night = Night(night_date.year, night_date.month, night_date.day)
        number_str = f"{star_number:04}"
        folder = (
            self._night.path
            / "Flux Logs Combined"
            / self.get_radius_folder_name(radius)
        )
        candidates = list(folder.glob(f"*-{number_str}_flux.txt"))
        if len(candidates) == 0:
            raise ValueError(f"Fluxlog combined no. {number_str} not found in {folder}")
        elif len(candidates) > 1:
            raise ValueError(f"Multiple candidates for no. {number_str} in {folder}")
        candidate = candidates[0]
        self._path = candidate
        self._data = None

    def is_valid_file_name(self):
        return bool(self.file_name_re.match(self.path.name))

    def image_number(self):
        if not self.is_valid_file_name():
            raise ValueError(f"{self.path.name} doesn't match naming conventions")
        return self.extract_image_number(self.path.name)

    @property
    def data(self):
        if self._data is None:
            self._data = pd.read_csv(self.path, skiprows=5, delim_whitespace=True)
        return self._data

    @property
    def path(self):
        return self._path

    @property
    def night(self):
        return self._night

    def __lt__(self, other):
        return self.image_number() < other.image_number()

    def __neq__(self, other):
        return self.image_number() != other.image_number()

    def __eq__(self, other):
        return self.image_number() == other.image_number()

    def __str__(self):
        return f"{self._night}. {self.path.name}"

    def __repr__(self):
        return self.path.name
