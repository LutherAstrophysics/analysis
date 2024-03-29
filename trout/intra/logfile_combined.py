import re
from datetime import date
from functools import total_ordering

import pandas as pd


@total_ordering
class LogFileCombined:
    file_name_re = re.compile(r"(\d{2}-\d{2}-\d{2})_m23_(\d+\.\d*)-(\d{3})\.txt")

    @classmethod
    def extract_image_number(cls, name):
        return int(cls.file_name_re.match(name)[3])

    def __new__(cls, night_date: date, number: int):
        """
        Ensures each logfile combined instance is a singleton.
        """
        if not hasattr(cls, "files"):
            cls.files = {}
        year, month, day = night_date.year, night_date.month, night_date.day
        assert (type(year), type(month), type(day)) == (int,) * 3
        assert (type(number)) == int
        identifier = (year, month, day, number)
        if not cls.files.get(identifier):
            cls.files[identifier] = super(LogFileCombined, cls).__new__(cls)
        return cls.files[identifier]

    def __init__(self, night_date: date, number: int):
        from .night import Night
        self._night = Night(night_date.year, night_date.month, night_date.day)
        number_str = f"{number:03}"
        folder = self._night.path / "Log Files Combined"
        candidates = list(folder.glob(f"*-{number_str}.txt"))
        if len(candidates) == 0:
            raise ValueError(f"Logfile no. {number_str} not found in {folder}")
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
            self._data = pd.read_csv(
                self.path, skiprows=8, delimiter=r"\s{2,}", engine="python"
            )
            self._data.index = [i+1 for i in self._data.index]
            self._data.index.name = "Star_no"
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
