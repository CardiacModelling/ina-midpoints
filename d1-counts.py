#!/usr/bin/env python3
#
# Calculates statistics about the standard deviations reported in the midpoints
# data.
#
import numpy as np

import base

with base.connect() as con:
    c = con.cursor()

    # Count total number of reports (1 or more per publication)
    row = next(c.execute('select count(pub) from midpoints_wt'))
    print(f'Total reports: {row[0]}')

    # Count total number of publications
    row = next(c.execute('select count(distinct(pub)) from midpoints_wt'))
    print(f'Total publications: {row[0]}')

