#!/usr/bin/env python3
#
# Creates data for a funnel plot, showing SEM as a function of Vi or Va.
#
import os

import base


with base.connect() as con:
    q = 'select pub from midpoints_wt'
    rows = con.execute(q)
    #path = os.path.join(base.DIR_DATA_OUT, 'maxi.csv')
    path = 'maxi.csv'
    print(f'Writing to {os.path.relpath(path)}')
    with open(path, 'w') as f:
        csv = base.csv_writer(f)
        csv.writerow(['pub', 'maxi'])
        for row in rows:
            csv.writerow([row[0], -1000])

