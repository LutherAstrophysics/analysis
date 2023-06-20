from datetime import datetime
from typing import Iterable, Union

import numpy as np

from trout.constants import BAD_NIGHTS_DATE_FORMAT
from trout.stars import Star


def get_nights_ltpr_values(
    year: int,
    stars_to_use: Iterable[int],
    attendance_threshold: float,
    is_primary: bool = True,
):
    """
    Returns a dictionary of the nights with their ltpr(aka. badness) value for a year by looking
    at the data from stars in `stars_to_use`

    param: year: Year to analyze
    param: stars_to_user:
        The list of stars to use for calculation of bad nights
        Note that you should not provide the variable stars in this list
    param: attendance_threshold:
        Stars with less this stated threshold will not be considered when doing
        calculation
    param: Whether to calculate badness value for the primary or the secondary dataset
    """

    season_mean_signal = {}
    nightly_ratio = {}

    for star in stars_to_use:
        star_data = Star(star, is_primary)

        # Skip the star if it doesn't pass attendance threshold
        if star_data.attendance(year) < attendance_threshold:
            continue

        # Select only the data for the year
        star_data.select_year(
            year,
            exclude_bad_nights=False,  # Important to include all nights
            exclude_zeros=True,
        )

        # Save mean for the star for the year
        season_mean_signal[star] = star_data.mean()

        for (
            _,
            flux,
            date,
        ) in star_data.selected_data:  # Note this is different from star_selected_data
            night_name = date.strftime(BAD_NIGHTS_DATE_FORMAT)
            ratio_for_star_for_night = flux / season_mean_signal[star]

            # Add this ratio to the nightly_ratio
            nightly_ratio.setdefault(night_name, [ratio_for_star_for_night]).append(
                ratio_for_star_for_night
            )

    nightly_ratios_std = {}
    for night, ratios in nightly_ratio.items():
        ratios = np.array(ratios)
        nightly_ratios_std[night] = np.std(ratios)

    return nightly_ratios_std


def _get_ltpr_threshold(year: int):
    """
    Returns the LTPR aka. badness threshold to use
    for the given year
    """
    if 2003 <= year <= 2006:
        return 0.035
    elif 2007 <= year <= 2008:
        return 0.045
    else:
        return 0.035


def calc_bad_nights(
    year: int,
    /,
    *,
    attendance_threshold: float = 0.5,
    ltpr_threshold: Union[float, None] = None,
    stars_to_use: Union[Iterable[int], None] = None,
    is_primary: bool = True,
    silent: bool = False,
    show_all_ltpr_values: bool = False,
):
    """
    Calculates bad nights for the given year.
    Prints the statistics to standard out

    @param year: year for which to calculate bad nights
    @attendance_threshold: minimum attendance (between 0 and 1) for the star (optional)
    @ltpr_threshold: ltpr threshold above which to consider a night as bad
    @stars_to_use: List of stars to use (optional)
    @is_primary: Whether to consult primary of secondary database
    @silent: boolean indicating whether the you want to disable output on stdin
    @show_all_ltpr_values: boolean indicating whether the you want to see LTPR
    values for all nights (default false)

    If you want the ltpr values for a year to play with, call the
    `get_nights_ltpr_values` function instead

    WARNING
    Also note that this is very different form the `trout.nights.bad_nights`
    function which just returns the list of bad nights from our database. This
    function should be used to calculate the list of bad nights. Once you have
    done that once, you should upload it to the database and call the much
    faster `trout.nights.bad_nights` function.

    """
    # returns iterable of night date that have LTPR above the threshold

    # The basic idea for this program is:
    # Create a list for stars to process, call is `stars_to_process`
    # Add stars 1-1000 to stars_to_process
    # Throw out variable stars from `stars_to_process`
    # Throw out stars that have <80% attendance for the year from `stars_to_process`

    # Create a dictionary, call it `season_mean_signal` to hold mean signals of
    # stars for the entire data season
    #   Note that the mean signal for a season for a stars is calculated from
    #   set of the internight normalized signal on each night of the season for
    #   the star.  For each night, create a dictionary to hold data for the
    #   night, call it `nights_data_dict` Create a entry in the dictionary with
    #   the night_date as key and the value as the list containing: The ratio of
    #   signal_of_star_on_night[night] / season_mean_signal[star_i] for each
    #   star For each night, create a dict to hold std of values in
    #   `nights_data_dict`, call this dict `nights_signal_std_dict` (note that
    #   at this point, we have a standard deviation value for each night) We
    #   mark nights that have this value above a threshold (example: 0.035 for
    #   old camera, 0.03 for new camera) as bad nights for the year

    if stars_to_use is None:
        stars_to_use = get_default_stars_to_include()
    if ltpr_threshold is None:
        ltpr_threshold = _get_ltpr_threshold(year)

    if not silent:
        print("Year:", year)
        print("Attendance threshold:", attendance_threshold)
        print("LTPR threshold:", ltpr_threshold)
        print("Primary Dataset:", is_primary)

    bad_nights_list = []
    badness_data = get_nights_ltpr_values(
        year, stars_to_use, attendance_threshold, is_primary
    )

    if show_all_ltpr_values:
        print("\n")
        print(f"{'Night':<20s}", f"{'LTPR':<10s}")

    for night, badness in sorted(
        badness_data.items(),
        key=lambda x: datetime.strptime(x[0], BAD_NIGHTS_DATE_FORMAT).toordinal(),
    ):
        if show_all_ltpr_values:
            print(f"{str(night):<20s}", f"{badness:<10.6f}")
        if badness > ltpr_threshold:
            bad_nights_list.append(night)

    if not silent:
        print(
            """
==============
Bad nights
==============
"""
        )
        print(bad_nights_list)

    return bad_nights_list


def get_default_stars_to_include():
    """
    Returns default stars to use
    """
    stars_to_exclude = [
        1,
        16,
        41,
        69,
        82,
        100,
        115,
        138,
        166,
        168,
        195,
        245,
        255,
        281,
        285,
        294,
        317,
        332,
        338,
        356,
        357,
        366,
        377,
        410,
        414,
        441,
        465,
        466,
        504,
        533,
        539,
        592,
        597,
        600,
        628,
        635,
        664,
        672,
        685,
        697,
        703,
        722,
        736,
        753,
        755,
        777,
        788,
        790,
        814,
        824,
        842,
        850,
        852,
        870,
        877,
        879,
        888,
        892,
        904,
        908,
        912,
        929,
        950,
        958,
        981,
        1007,
        1048,
        1052,
        1054,
        1065,
        1103,
        1113,
        1131,
        1143,
        1144,
        1191,
        1195,
        1197,
        1219,
        1223,
        1276,
        1369,
        1426,
        1475,
        1495,
        1529,
        1539,
        1654,
        1687,
        1693,
        1702,
        1716,
        1843,
        1856,
        1873,
        1887,
        2237,
        2251,
        2252,
        2502,
        2509,
        2510,
    ]  # noqa
    stars_to_include_default = list(range(1, 1000))
    return list(filter(lambda x: x not in stars_to_exclude, stars_to_include_default))
