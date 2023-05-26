# Boilerplate to allow importing `trout`
import sys

if "../" not in sys.path:
    sys.path.append("../")


# Write your code here

from trout.vis import field

field()
