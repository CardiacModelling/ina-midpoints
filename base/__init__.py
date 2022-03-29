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

# Root directory
DIR_ROOT = os.path.abspath(os.path.join(DIR, '..'))

# Data input files
DIR_DATA_IN = os.path.join(DIR_ROOT, 'data-in')

# Data output files
DIR_DATA_OUT = os.path.join(DIR_ROOT, 'data-out')

# DB file
PATH_DB = os.path.join(DIR_DATA_IN, 'mutations.sqlite')

# Ensure output paths exist
if not os.path.isdir(DIR_DATA_OUT):
    print(f'Creating directory {DIR_DATA_OUT}')
    os.makedirs(DIR_DATA_OUT)

# Delete imported libraries
del(os, inspect)


# CSV File options
CSV_OPTIONS = {
    'delimiter': ',',
    'quotechar': '"',
    'skipinitialspace': True,
}


def csv_writer(filehandle):
    """
    Returns a csv writer for the given filehandle, initialized with the
    default options.
    """
    import csv
    return csv.writer(filehandle, **CSV_OPTIONS)


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
from ._connection import connect    # noqa

