from typing import Union

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from trout.constants import STAR_TABLE_HEADER
from trout.conversions import flux_to_magnitude_4px
from trout.database import query
from trout.exceptions import InvalidStarNumberError, InvalidQueryError
from trout.stars.utils import is_valid_star, star_table_name, get_star_data

from .utils import bad_nights_filtered_data

class Star:
    """
    A star object, useful for viewing data for the star, advanced filtering of
    data and drawing scatter plot of the data. 
    """

    def __init__(self, number: int):
        if not is_valid_star(number):
            raise InvalidStarNumberError
        self._number = number
        self._data = get_star_data(number)
        self._table = star_table_name(self.number)

        # Headers match the column names in the database
        # These are the column names to use to filter data
        self._headers = list(map(lambda x : x[0],
            sorted(STAR_TABLE_HEADER.items(), key=lambda x : x[1])))

        self._selected_data = []

    @property
    def headers(self):
        return self._headers

    @property
    def number(self):
        return self._number
    
    @property
    def selected_data(self):
        return self._selected_data

    def peek(self):
        """
        Take a look at first few items of the data.
        """
        return self._data[:5]

    def select(self, filter_query="", exclude_bad_nights : bool=True,
            exclude_zeros : bool = True):
        """
        Filters a portion of the data to be used during plotting. Filtering is
        based on the the Postgresql syntax where filter_query is the string to
        use after there WHERE keyword

        param: filter_query: Filter to use
        param: exclude_bad_nights: Whether or not to filter bad nights, default
               True
        param: exclude_zeros: Whether or not to exclude nights with no data
        return: self

        Examples:

        x.select("date > '2005-01-01'") selects only those datapoints past
        2005-01-01.

        x.select("date > '2005-01-01' and date <= '2015-05-05'") selects only
        those datapoints after 2005-01-01 and before 2015-05-06.

        x.select("flux > 1650000") selects only those datapoints with flux
        greater than 165000

        Or you could even combine the flux and the date together like:
        x.selecte("flux > 1700000 and date < '2010-01-01'")

        Note that x is the Star object in these examples

        To reset the selection to all data, you may call this function without
        any parameters
        """
        try:
            if filter_query:
                # Tuple used for enforcing immutabilty
                self._selected_data = tuple(query(f"SELECT * FROM {self._table} WHERE {filter_query}"))
            else:
                # Reset when called without filter_query or a False(y) value
                # like the empty string
                self._selected_data = query(f"SELECT * FROM {self._table}")

            # Filter bad nights if necessary
            if exclude_bad_nights:
                self.filter_bad_nights()

            # Filter zero points if necessary
            if exclude_bad_nights:
                self.filter_zeros()

            return self
        except:
            raise InvalidQueryError
    
    def transform_selected(self, flux_transformation_fn = lambda x :
            x[STAR_TABLE_HEADER['flux']]):
        """
        Transform the flux with some transformation function provided.
        Note that this ony alters the selected_data field. 
        If you want to reset the data, just call the select method without any
        parameters.

        param: flux_transformation_fn: Function that takes old data (tuple of
            id, flux value and date) and returns new flux value. 
            Its default value is identify function in the sense that it leaves the 
            flux value unaltered. Technically it is a function that take a tuple and
            returns item in the second position (which is where flux is stored)
        return: the transformed dataset

        Examples:
        Say you want to double the magnitude of all datapoints taken before 2009
        feb and keep the magnitude of other datapoints intact, you would then write
        your transformation function first

        def transform(data):
            # Break the tuple
            sn, flux, date = data

            import datetime # for date comparison
            if date < datetime.date(2009, 2, 1):
                return flux * 2
            else:
                return flux

        then you would call this method with the newly created transformation
        function as follows:

        x.transform_selected(transform)

        Note that the transformation is done in the x.selected_data so if that's
        not set your result of transformation will also be empty.
        """
        transformed_data = []
        for index, data in enumerate(self.selected_data):
            sn, flux_o, date = data
            transformed_data.append((sn, flux_transformation_fn(data), date))
        # Update _selected_data
        # Tuple used for enforcing immutabilty
        self._selected_data = tuple(transformed_data)

    def plot(self, title=None):
        """
        Pots a scatter from the selected_data. If the selected_data is empty,
        then no plot will be drawn.

        param: (optional) title: The title of the plot.
        return: None
        """
        flux_column, date_column = STAR_TABLE_HEADER['flux'], STAR_TABLE_HEADER['date'], 
        # Filter to remove data where flux <= 0
        data = list(filter(lambda x : x[flux_column] > 0, self.selected_data))

        # Nothing to plot if there is no data.
        if len(data) != 0:
            # Create np array of data
            data = np.array(data)
            flux, date = data[:, flux_column], data[:, date_column]
            mags = list(map(flux_to_magnitude_4px, flux))

            # Plot axis: (x, y) 
            # Plot option: 'ro' means red circle for each datapoint
            # Plot option: ms is for marker size
            plt.plot(date, mags, 'ro', ms=2.5)
            # Format Axis
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 
            plt.gcf().autofmt_xdate() # Fit date
            plt.xlabel('Date')
            plt.ylabel('Magnitude')
            # Invert the magnitude axis
            plt.gca().invert_yaxis()

            # Set the size of figure to 10X5 inch
            plt.rcParams["figure.figsize"] = (10,5)

            # Set title for the plot
            if title:
                plt.title(title)
            else:
                plt.title(self.__repr__())
            plt.show()

    def attendance(self, year : Union[int, None] = None, print_stats=False) -> float:
        """
        Calcualtes the attendance % of the star. The attendace is calculated 
        after removing the bad nights.

        param: (optional) year for which to calculate attendance. Default to all
                years
        return: the attendance percentage in given year or the entire period 
        """
        if year is None:
            data = query(f"SELECT * FROM {self._table}")
        elif type(year) != int:
            raise ValueError("Invalid year value")
        else:
            data = query(f"SELECT * FROM {self._table} where date >= '{year}-01-01' and date < '{year + 1}-01-01'")
        data_points = len(data)
        # Filter bad nights
        data = bad_nights_filtered_data(data)
        data_points_bad_nights_removed = len(data)
        # Data after removing zeros (nights where star is absent)
        data_cleaned = list(filter(lambda x : x[1] > 0, data))
        if print_stats:
            print(f"Data points: {data_points}")
            print(f"Data points (excluding bad nights): {data_points_bad_nights_removed}")
            print(f"Attended nights (without bad nights): {len(data_cleaned)}")
        if data_points == 0:
            raise ValueError(f"Year {year} doesnt exist")
        return  len(data_cleaned) / data_points_bad_nights_removed 


    def filter_bad_nights(self):
        """
        Filter bad nights from selected_data. Note that this method doesn't
        return anything but alters the value of self.selected_data

        return : None
        """
        self._selected_data = bad_nights_filtered_data(self._selected_data)

    def filter_zeros(self):
        """
        Filter zero points from selected_data. Note that this method doesn't
        return anything but alters the value of self.selected_data

        return : None
        """
        self._selected_data = list(filter(lambda x : x[1] > 0, self._selected_data))

    def __str__(self):
        return self

    def __repr__(self):
        return f"Star: {self.number} Datapoints: {len(self._data)} Selected: {len(self.selected_data)}"
