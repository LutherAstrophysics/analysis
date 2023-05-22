The `analysis` package in this repo is made available in the JUPYTER
notebook served at
<http://10.30.5.4/>.

To make that possible, all
requirements mentioned in this packages's requirements.txt are also
installed by default for all users in their JUPYTER environment.

Note that the name of this package is `trout` and the usage is as
follows:

```
# Import
from trout.stars import get_star
from trout.nights import bad_nights
from trout.nights.year_nights import get_nights_in_a_year

# Use
foo = get_star(2) # Gets star from primary data source
bar = get_star(2, is_primary=False) # Gets star from secondary source

bar.select()
bar.plot()

print(foo)
print(foo._data)

foo.select("date >= '2013-01-01' and date < '2014-01-01'") # Select only 2013 data
# Selecting a year can alternatively be done by
# foo.select_year(2013)


# Plot selected data
foo.plot()

# Get mean, median, min, max of selected data (2013 in our case)
print(foo.mean(), foo.median(), foo.min(), foo.max())


# Select 2015 including bad nights
foo.select_year(2015, exclude_bad_nights=False)
foo.plot()

# Get step from 2010 to 2011
step_ratio = foo.step(2010, 2011) # 2011 mean / 2010 mean
if step_ratio > 1:
  print("Brightness increased in 2011 from 2010")
# Note that you may calculate step between two non-consecutive years.
step_ratio_first_last = foo.step(2003, 2022) # 2022 mean / 2003 mean


primary_data_nights_2020 = get_nights_in_a_year(2020)
secondary_data_nights_2020 = get_nights_in_a_year(2020, is_primary=False)

bad_nights_primary = bad_nights() # All bad nights in primary data source
bad_nights_primary_peek = bad_nights(10) # First 10 bad nights in primary data source
bad_nights_secondary = bad_nights(is_primary=False) # All bad nights in secondary data source
bad_nights_secondary_peek = bad_nights(10, is_primary=False) # First 10 bad nights in secondary data source
```

Some examples of data analysis can be found here:
<https://github.com/LutherAstrophysics/suman-analysis>


## Updating

To update this package and have the updates reflected in server's Jupyter.
1. Push your change to github.
1. git pull in the server's desktop folder named analysis.
1. Shutdown all running instances of jupyter notebook by going to "Running tab"
1. If still the changes aren't reflected, you might have to restart the server.

## Primary and secondary data source
