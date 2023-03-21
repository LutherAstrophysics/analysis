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
from trout.greet import hello

# Use
hello()
```

Please make sure that you do a git pull in the server's desktop folder
where this package is cloned to get new updates to the package
reflected in our jupyter notebook. You might also have to restart the
Jupyter notebook session (perhaps closing the tab and opening it again
will do) once you make updates. Or you might have to go _Shutdown_ all
running notebooks in the running tabs in the Jupyter Server and
open the required notebook again.


## Primary and secondary data source