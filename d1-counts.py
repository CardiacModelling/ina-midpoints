#!/usr/bin/env python3
#
# Calculates statistics about the standard deviations reported in the midpoints
# data.
#
import base


with base.connect() as con:
    c = con.cursor()

    # Count total number of reports (1 or more per publication)
    row = next(c.execute('select count(pub) from midpoints_wt'))
    print(f'Total reports: {row[0]}')

    # Count total number of publications
    row = next(c.execute('select count(distinct(pub)) from midpoints_wt'))
    print(f'Total publications: {row[0]}')

    # Count Va measurements
    row = next(c.execute('select count(va) from midpoints_wt where na > 0'))
    print(f'Total Va reports: {row[0]}')

    # Count Vi measurements
    row = next(c.execute('select count(vi) from midpoints_wt where ni > 0'))
    print(f'Total Vi reports: {row[0]}')

    # Count Va + Vi measurements
    row = next(c.execute(
        'select count(vi) from midpoints_wt where ni > 0 and na > 0'))
    print(f'Total Va+Vi reports: {row[0]}')

