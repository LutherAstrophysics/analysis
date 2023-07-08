import re
from datetime import date
from functools import total_ordering

import matplotlib.pyplot as plt
import numpy as np
from astropy.io.fits import getdata
from matplotlib.colors import LogNorm


@total_ordering
class AlignedCombined:
    file_name_re = re.compile(r"m23_(\d+\.?\d*)[-_](\d+).fit")

    @classmethod
    def extract_image_number(cls, name):
        return int(cls.file_name_re.match(name)[2])

    def __new__(cls, night_date: date, number: int):
        """
        Ensures each aligned combined instance is a singleton.
        """
        if not hasattr(cls, "files"):
            cls.files = {}
        year, month, day = night_date.year, night_date.month, night_date.day
        assert (type(year), type(month), type(day)) == (int,) * 3
        assert (type(number)) == int
        identifier = (year, month, day, number)
        if not cls.files.get(identifier):
            cls.files[identifier] = super(AlignedCombined, cls).__new__(cls)
        return cls.files[identifier]

    def __init__(self, night_date: date, number: int):
        from .night import Night

        self._night = Night(night_date.year, night_date.month, night_date.day)
        number_str = f"{number:04}"
        folder = self._night.path / "Aligned Combined"
        candidates = list(folder.glob(f"*{number_str}.fit"))
        if len(candidates) == 0:
            raise ValueError(f"AlignedCombined no. {number_str} not found in {folder}")
        elif len(candidates) > 1:
            raise ValueError(f"Multiple candidates for no. {number_str} in {folder}")
        candidate = candidates[0]
        self._path = candidate
        self._data = None

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        ticks = np.arange(0, 1023, 64)

        ax.set_xticks(ticks, minor=True)
        ax.set_yticks(ticks, minor=True)

        ax.grid(which="both")
        ax.grid(which="minor", alpha=0.2)
        ax.grid(which="major", alpha=0)

        x = ax.imshow(self.data, cmap="gray", norm=LogNorm())

        # Plot Star 1 just for reference
        ax.scatter([746.58], [459.64], color="r")
        ax.text(700, 459, "#1: 746.58, 459.64")

        fig.colorbar(x)
        plt.title(f"{self._night}-{self}")
        plt.show()

    def is_valid_file_name(self):
        return bool(self.file_name_re.match(self.path.name))

    def image_number(self):
        if not self.is_valid_file_name():
            raise ValueError(f"{self.path.name} doesn't match naming conventions")
        return self.extract_image_number(self.path.name)

    @property
    def data(self):
        if self._data is None:
            self._data = getdata(self.path)
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
