#!/usr/bin/env python3
#
# Calculates how many reports mentioned the LJP
#
import numpy as np

import base

qand = ' cell != "Oocyte" group by pub'

# Query db
with base.connect() as con:
    c = con.cursor()

    q = f'select ljp, ljp_corrected from midpoints_wt where {qand}'

    yes, no, un = 0, 0, 0
    rows = [row for row in c.execute(q)]
    for row in rows:
        ljpc = row['ljp_corrected']
        if ljpc is None:
            un += 1
        elif ljpc == 'yes':
            yes += 1
        else:
            no += 1

    f = 100 / len(rows)
    print(f'Yes {yes}, No {no}, No mention {un}')
    print(f'{f * yes}, {f * no}, {f * un}')

