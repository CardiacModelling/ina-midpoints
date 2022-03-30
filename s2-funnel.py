#!/usr/bin/env python3
#
# Creates data for a funnel plot, showing SEM as a function of Vi or Va.
#
import os

import numpy as np

import base


def gather(rows, filename):
    """
    Convert the data in ``rows`` (given as ``pub, v, sem, n, 1/sqrt(n)``) to
    CSV file ``filename``.
    """
    path = os.path.join(base.DIR_DATA_OUT, filename)
    print(f'Writing to {os.path.relpath(path)}')
    with open(path, 'w') as f:
        csv = base.csv_writer(f)
        csv.writerow(['pub', 'v', 'sem', 'n', 'inv-sqrt-n'])
        for row in rows:
            data = list(row)
            data.append(1 / np.sqrt(row[-1]))
            csv.writerow(data)


with base.connect() as con:
    q = 'select pub, va, sema, na from midpoints_wt where na > 0'
    rows = con.execute(q)
    gather(rows, 'midpoints-wt-va.csv')

    q = 'select pub, vi, semi, ni from midpoints_wt where ni > 0'
    rows = con.execute(q)
    gather(rows, 'midpoints-wt-vi.csv')

