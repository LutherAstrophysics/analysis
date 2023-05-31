import re
from collections import namedtuple
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Union

import numpy as np
import numpy.typing as npt


# Note that LogFileCombined is the one that that has the data for aligned combined
# images after extracting stars from the image. This is not to be confused with FluxLogCombined
# that is created after intra-night normalization (note *not* internight normalization)
class LogFileCombinedFile:
    # Class attributes
    header_rows = 9
    data_titles_row_zero_index = 8
    date_format = "%m-%d-%y"
    sky_adu_column = 5
    x_column = 0
    y_column = 1
    file_name_re = re.compile("(\d{2}-\d{2}-\d{2})_m23_(\d+\.\d*)-(\d{3})\.txt")
    star_adu_radius_re = re.compile("Star ADU (\d+)")

    StarLogfileCombinedData = namedtuple(
        "StarLogfileCombinedData",
        ["x", "y", "xFWHM", "yFWHM", "avgFWHM", "sky_adu", "radii_adu"],
    )
    LogFileCombinedDataType = Dict[int, StarLogfileCombinedData]

    @classmethod
    def generate_file_name(cls, night_date: date, img_no: int, img_duration: float):
        """
        Returns the file name to use for a given star night for the given night date
        param : night_date: Date for the night
        param: img_no : Image number corresponding to the Aligned combined image
        param: img_duration : the duration of images taken on the night
        """
        return (
            f"{night_date.strftime(cls.date_format)}_m23_{img_duration}-{img_no:03}.txt"
        )

    def __init__(self, file_path: str) -> None:
        self.__path = Path(file_path)
        self.__is_read = False
        self.__data = None
        self.__title_row = None

    def _read(self):
        with self.__path.open() as fd:
            lines = [line.strip() for line in fd.readlines()]
            # Save the title row
            # We split the title row by gap of more than two spaces
            self.__title_row = re.split(
                r"\s{2,}", lines[self.data_titles_row_zero_index]
            )
            lines = lines[self.header_rows:]  # Skip headers - 1
            # Create a 2d list
            lines = [line.split() for line in lines]
            # Convert to 2d numpy array
            self.__data = np.array(lines, dtype="float")
        self.__is_read = True

    def _title_row(self):
        if not self.__is_read:
            self._read()
        return self.__title_row

    def _adu_radius_header_name(self, radius: int):
        return f"Star ADU {radius}"

    def _get_column_number_for_adu_radius(self, radius: int):
        titles = self._title_row()
        return titles.index(self._adu_radius_header_name(radius))

    def is_valid_file_name(self) -> bool:
        """
        Checks if the filename matches the naming convention
        """
        return bool(self.file_name_re.match(self.path().name))

    def night_date(self) -> Union[date, None]:
        """
        Returns the night date that can be inferred from the file name
        """
        if self.is_valid_file_name():
            # The first capture group contains the night date
            return datetime.strptime(
                self.file_name_re.match(self.path().name)[1],
                self.date_format,
            ).date()

    def get_adu(self, radius: int):
        """
        Returns an ordered array of ADU for stars for given `radius`.
        The first row of the array is the adu of star 1, 200th row for star 200,
        and the like
        """
        radius_col = self._get_column_number_for_adu_radius(radius)
        return self.data()[:, radius_col]

    def get_sky_adu_column(self):
        """
        Returns an ordered array of stars sky adu.
        The first row of the array is the sky adu of star 1, 200th row for star 200,
        and the like
        """
        return self.data()[:, self.sky_adu_column]

    def get_x_position_column(self):
        """
        Returns an ordered array of stars x positions.
        The first row of the array is the x position of star 1, 200th row for star 200,
        and the like
        """
        return self.data()[:, self.x_column]

    def get_y_position_column(self) -> npt.NDArray:
        """
        Returns an ordered array of stars y positions.
        The first row of the array is the y position of star 1, 200th row for star 200,
        and the like
        """
        return self.data()[:, self.y_column]

    def get_star_data(self, star_no: int) -> StarLogfileCombinedData:
        """
        Returns the details related to a particular `star_no`
        Returns a named tuple `StarLogfileCombinedData`
        """
        star_data = self.data()[star_no - 1]
        titles = self._title_row()
        first_radii_adu_column = 6
        radii_adu = {}
        for index, col_name in enumerate(titles[first_radii_adu_column:]):
            radius = int(self.star_adu_radius_re.match(col_name)[1])
            radii_adu[radius] = star_data[first_radii_adu_column + index]
        return self.StarLogfileCombinedData(
            *star_data[:first_radii_adu_column], radii_adu
        )

    def img_duration(self) -> Union[float, None]:
        """
        Returns the image duration that can be inferred from the file name
        """
        if self.is_valid_file_name():
            # The second capture group contains the image duration
            return float(self.file_name_re.match(self.path().name)[2])

    def img_number(self) -> Union[int, None]:
        """
        Returns the image number associated to the filename if the file name is valid
        """
        if self.is_valid_file_name():
            # The third capture group contains the image number
            return int(self.file_name_re.match(self.path().name)[3])

    def is_file_format_valid(self):
        """
        Checks if the file format is valid
        """
        return True

    def path(self):
        return self.__path

    def data(self):
        if not self.__is_read:
            self._read()
        return self.__data

    def __len__(self):
        """Returns the number of stars present in the dataset"""
        return len(self.data())

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Log file combined: {self.__path}"
