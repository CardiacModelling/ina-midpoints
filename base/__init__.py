#!/usr/bin/env python3
#
# Database module (adapted from SCN5A mutations project).
#

# Module directory
import os
import inspect
try:
    frame = inspect.currentframe()
    DIR = os.path.realpath(os.path.dirname(inspect.getfile(frame)))
finally:
    del frame

# DB file
PATH_DB = os.path.join(DIR, 'mutations.sqlite')

# Delete imported libraries
del os, inspect


#
# Import functions and classes
#
from ._connection import (  # noqa
    connect,
)
from ._plot import (        # noqa
    axletter,
)
