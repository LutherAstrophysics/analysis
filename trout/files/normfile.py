import pandas as pd
import pkg_resources


class NormFile:
    idl_normfile = None

    @classmethod
    def get_idl_normfile(cls):
        """
        Returns the Internight normalization file, dataframe
        """
        file_path = pkg_resources.resource_filename(
            "trout", "data/idl_internorm_08-04-03_m23_3.5_071.txt"
        )
        df = pd.read_csv(
            file_path,
            delim_whitespace=True,
            skiprows=9,
            names=["x", "y", "sigma", "fwhm", "sky_adu", "adu_4", "adu_3"],
        )

        # Add star number column
        df["star"] = range(1, len(df) + 1)

        # Bring star number column to the front
        cols = df.columns.tolist()
        cols = ["star"] + cols[:-2]
        df = df[cols]
        return df
