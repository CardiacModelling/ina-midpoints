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
    del(frame)

# DB file
PATH_DB = os.path.join(DIR, 'mutations.sqlite')

# Delete imported libraries
del(os, inspect)


def table(head, rows):
    """
    Prints a table based on the given ``head`` and ``rows``.
    """
    if len(rows) > 0:
        if len(head) != len(rows[0]):
            raise ValueError('Head and rows must have same column count.')

    # Get formats
    fmats = []
    for x in rows[0]:
        if isinstance(x, int):
            fmats.append('{:d}')
        elif isinstance(x, float):
            fmats.append('{:8.5g}')
        else:
            fmats.append('{:s}')

    # Format cells
    widths = [len(x) for x in head]
    cells = [head]
    for row in rows:
        row = [f.format(x) for f, x in zip(fmats, row)]
        for i, x in enumerate(row):
            if len(x) > widths[i]:
                widths[i] = len(x)
        cells.append(row)
    rows = cells

    # Print table
    for row in rows:
        line = []
        for x, w in zip(row, widths):
            line.append(' ' * (w - len(x)) + x)
        print(' | '.join(line))


#
# Import functions and classes
#
from ._connection import (  # noqa
    connect,
)
from ._analysis import (    # noqa
    combined_pdf,
    individual_pdfs,
)
from ._plot import (        # noqa
    axletter,
)
