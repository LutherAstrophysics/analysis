from datetime import datetime
from functools import total_ordering
from pathlib import Path
from typing import Iterable

from trout.intra import DATA_DRIVE

from .night import Night


@total_ordering
class Year:
    @classmethod
    def make_year_path(self, year: int):
        return Path(DATA_DRIVE) / str(year)

    def __new__(cls, year: int):
        """
        Ensures each year instance is a singleton.
        """
        if not hasattr(cls, "years"):
            cls.years = {}
        assert type(year) == int
        if not cls.years.get(year):
            cls.years[year] = super(Year, cls).__new__(cls)
        return cls.years[year]

    def __init__(self, year: int):
        self._year = year
        self._path = self.make_year_path(year)
        if not self._path.exists():
            raise ValueError(f"{year} data doesn't exist in", DATA_DRIVE)
        self._nights = None

    @property
    def nights(self) -> Iterable[Night]:
        if self._nights is None:
            nights = []
            for f in self.path.glob("*"):
                name = f.name
                if Night.matches_name(f.name):
                    night_date = datetime.strptime(name, Night.NAME_FORMAT)
                    year, month, day = night_date.year, night_date.month, night_date.day
                    nights.append((night_date, Night(year, month, day)))
            _, nights_sorted = zip(*sorted(nights, key=lambda x: x[0]))
            self._nights = nights_sorted
        return self._nights

    @property
    def year(self):
        return self._year

    @property
    def path(self):
        return self._path

    def __lt__(self, other):
        return self.year < other.year

    def __neq__(self, other):
        return self.year != other.year

    def __eq__(self, other):
        return self.year == other.year

    def __str__(self):
        return f"Year: {self.year}"

    def __repr__(self):
        return self.year
