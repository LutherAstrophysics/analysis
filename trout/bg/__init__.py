import re
from datetime import date, datetime
from functools import cache
from typing import Union

import ephem
import pandas as pd


class SKY:
    """
    Class to help analyze sky background data files
    from google sheets in the format
    https://docs.google.com/spreadsheets/d/1VicH9PPi2jk4bWxQ4X-S62CHyFNpfHlye9KBFQH5woU/edit#gid=0

    Note that this class is currently unstable and might change
    in the future without maintaining backwards compatibility
    """

    date_pattern = re.compile(r"\[([\d\/]+)\]\s*\[([0-9:]+).*")

    @classmethod
    def format_date_string(cls, date_str) -> str:
        match = cls.date_pattern.match(date_str)
        date, time = match[1], match[2]
        return date + " " + time

    def __init__(self, url):
        self._url = url
        self.df = self._get_df()

        # Format into date and time
        self.df["date"] = pd.to_datetime(
            self.df["date"].apply(self.format_date_string), format="%m/%d/%Y %I:%M:%S"
        )

    def _get_csv_link(self):
        return self._url.replace("/edit#gid=", "/export?format=csv&gid=")

    def _get_df(self):
        url = self._get_csv_link()
        return pd.read_csv(url)


class SkyNew:
    """
    This newer class (compared to Sky) class above relies on the data in these
    google sheets
    https://docs.google.com/spreadsheets/d/1IzFoILblEIWqDE5t31QmwQ4TSz7FeU0k7sdPlIoHeJE/edit#gid=894220236
    The data used here is generated from the night_csv, part of the `m23` package.
    """

    spreadsheet_id = "1IzFoILblEIWqDE5t31QmwQ4TSz7FeU0k7sdPlIoHeJE"

    def __init__(self, years, trim=True):
        if isinstance(years, int):
            years = [years]
        assert type(years) is list or type(years) is tuple
        self._years = years

        self._trim = trim

        all_dfs = []
        for year in years:
            url = self._get_csv_link(year)
            df = self._get_df(url)
            df.Date = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")
            all_dfs.append(df)

        self.df = pd.concat(all_dfs)

    @property
    def years(self):
        return self._years

    def _get_csv_link(self, year):
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/gviz/tq?tqx=out:csv&sheet={year}"  # noqa

    def _get_df(self, url):
        if self._trim:
            return pd.read_csv(url, usecols=lambda x: not x.split("_")[0].isdigit())
        else:
            return pd.read_csv(url)


@cache
def get_ephem_decorah_observer():
    decorah = ephem.Observer()

    decorah.lat = "43.3017"
    decorah.lon = "-91.79"

    decorah.elevation = 268
    return decorah


def get_next_astonomical_sunrise(date_of_observation: Union[datetime, date]) -> datetime:
    decorah_observer = get_ephem_decorah_observer()
    decorah_observer.date = date_of_observation.strftime("%Y-%m-%d")
    decorah_observer.horizon = "-18"  # Astronomical twilight

    to_return = decorah_observer.next_rising(ephem.Sun(), use_center=True)
    return datetime.strptime(to_return, "%Y/%m/%d HH:MM:SS")


def get_next_astonomical_sunset(date_of_observation: Union[datetime, date]) -> datetime:
    decorah_observer = get_ephem_decorah_observer()
    decorah_observer.date = date_of_observation.strftime("%Y-%m-%d")
    decorah_observer.horizon = "-18"  # Astronomical twilight

    to_return = decorah_observer.next_setting(ephem.Sun(), use_center=True)
    return datetime.strptime(to_return, "%Y/%m/%d HH:MM:SS")
