import re

import pandas as pd


class SKY:
    """
    Class to help analyze sky background data files
    from google sheets in the format
    https://docs.google.com/spreadsheets/d/1VicH9PPi2jk4bWxQ4X-S62CHyFNpfHlye9KBFQH5woU/edit#gid=0

    Note that this class is currently unstable and might change
    in the future without maintaining backwards compatibility
    """

    date_pattern = re.compile("\[([\d\/]+)\]\s*\[([0-9:]+).*")

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
