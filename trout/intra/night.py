from datetime import date, datetime
from functools import total_ordering

import pandas as pd

from trout.intra.aligned_combined import AlignedCombined
from trout.intra.flux_log_combined import FluxLogCombined
from trout.intra.logfile_combined import LogFileCombined
from trout.moon import phase, position
from trout.nights import bad_nights


@total_ordering
class Night:
    NAME_FORMAT = "%B %d, %Y"

    @classmethod
    def make_night_name(self, year: int, month: int, day: int):
        d = date(year, month, day)
        return d.strftime(self.NAME_FORMAT)

    @classmethod
    def matches_name(self, name):
        try:
            datetime.strptime(name, self.NAME_FORMAT)
            return True
        except ValueError:
            return False

    def __new__(cls, year: int, month: int, day: int):
        """
        Ensures each night instance is a singleton.
        """
        if not hasattr(cls, "years"):
            cls.nights = {}
        assert (type(year), type(month), type(day)) == (int,) * 3
        night_name = cls.make_night_name(year, month, day)
        if not cls.nights.get(night_name):
            cls.nights[night_name] = super(Night, cls).__new__(cls)
        return cls.nights[night_name]

    def __init__(self, year, month, day, year_instance=None):
        from .year import Year

        if not year_instance:
            year_instance = Year(year)
        assert year_instance.path.exists()
        assert type(year_instance) == Year
        self._night_date = date(year, month, day)
        self._night_name = self.make_night_name(year, month, day)
        self._path = year_instance.path / self._night_name
        if not self._path.exists():
            raise ValueError(
                f"{self._night_name} doesn't exist in {year_instance.path}"
            )
        self._year = year_instance
        self._aligned_combined = None
        self._logfiles_combined = None
        self._sky_bg = None
        self._alignment_stats = None
        self._color_normalized = {}

    def is_bad(self):
        """
        Checks whether the night is a bad night
        """
        _, bad_nights_for_year = zip(*bad_nights(year=self.night_date.year, is_primary=False))
        return self.night_date in bad_nights_for_year
    
    def has_color_normalized_folder(self):
        """
        Returns whether the night has color normalized folder Nights that didn't
        run through renorm potentially because of insufficient data points won't
        have this folder
        """
        f = self.path / "Color Normalized"
        return f.exists() and f.is_dir()

    def get_star_fluxlog_for_radius(self, star_no, radius: int):
        return FluxLogCombined(self.night_date, star_no, radius)

    def get_all_star_fluxlog_for_radius(self, star_no, radius: int):
        return FluxLogCombined(self.night_date, star_no, radius, all=True)

    def get_color_normalized(self, radius: int):
        if self._color_normalized.get(radius, None) is None:
            folder = (
                self.path
                / "Color Normalized"
                / FluxLogCombined.get_radius_folder_name(radius)
            )
            if not folder.exists():
                raise Exception(folder, "doesn't exist")
            candidates = list(folder.glob("*.txt"))
            if len(candidates) == 0:
                raise Exception("No matching file found.")
            elif len(candidates) > 1:
                raise Exception("Multiple candidates found")
            candidate = candidates[0]
            self._color_normalized[radius] = pd.read_csv(
                candidate,
                skiprows=2,
                delimiter=r"\s{2,}",
                engine="python",
                index_col=0,
            )  # C-engine doesn't support regex delimiter
        return self._color_normalized[radius]

    @property
    def stats(self):
        return {
            "moon_phase_name": phase(self.night_date),
            "moon_phase": position(self.night_date),
            # TODO: Humidity data
        }

    @property
    def sky_bg(self):
        if self._sky_bg is None:
            folder = self.path / "Sky background"
            candidates = list(folder.glob("*.txt"))
            if len(candidates) == 0:
                raise Exception("No matching file found.")
            elif len(candidates) > 1:
                raise Exception("Multiple candidates found")
            candidate = candidates[0]
            self._sky_bg = pd.read_csv(candidate, delim_whitespace=True)
        return self._sky_bg

    @property
    def alignment_stats(self):
        if self._alignment_stats is None:
            candidates = list(self.path.glob("*aligned_stats*.txt"))
            if len(candidates) == 0:
                raise Exception("No matching file found.")
            elif len(candidates) > 1:
                raise Exception("Multiple candidates found")
            candidate = candidates[0]
            self._alignment_stats = pd.read_csv(candidate, delim_whitespace=True)
        return self._alignment_stats

    @property
    def aligned_combined(self):
        if self._aligned_combined is None:
            folder = self.path / "Aligned Combined"
            files = []
            for f in folder.glob("*.fit"):
                file_name = f.name
                img_number = AlignedCombined.extract_image_number(file_name)
                files.append(AlignedCombined(self.night_date, img_number))
            self._aligned_combined = tuple(files)
        return sorted(self._aligned_combined)

    @property
    def logfile_combined(self):
        if self._logfiles_combined is None:
            folder = self.path / "Log Files Combined"
            files = []
            for f in folder.glob("*.txt"):
                file_name = f.name
                img_number = LogFileCombined.extract_image_number(file_name)
                files.append(LogFileCombined(self.night_date, img_number))
            self._logfiles_combined = tuple(files)
        return sorted(self._logfiles_combined)

    @property
    def path(self):
        return self._path

    @property
    def year(self):
        return self._year

    @property
    def night_name(self):
        return self._night_name

    @property
    def night_date(self):
        return self._night_date

    def __lt__(self, other):
        return self.night_date < other.night_date

    def __neq__(self, other):
        return self.night_date != other.night_date

    def __eq__(self, other):
        return self.night_date == other.night_date

    def __str__(self):
        return f"Night: {self.night_name}"

    def __repr__(self):
        return self.night_name
