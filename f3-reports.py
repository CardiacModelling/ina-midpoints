#!/usr/bin/env python3
#
# Creates data for a graph of V1/2 of activation & inactivation of wild-type
# channels in expression systems and myocyte data.
#
# Also writes t1-midpoints.tex
#
import os

import numpy as np
import scipy.stats

import base


'''

    # Gather data from rows
    for k, row in enumerate(rows):
        pub, v, sem, n, std = row
        field = str(k) + '-' + pub
        # Skip rows without act/inact measurement
        if n == 0:
            continue
        # Check std calculation
        if np.abs(std - sem * np.sqrt(n)) > 1e-6:
            print(f'Warning: Error in STD for {field}')
            print(f'  Listed    : {std}')
            print(f'  Calculated: {sem * np.sqrt(n)}')
        # Update ntotal
        ntotal += n
        # Store data
        fields.append(field)
        data[field] = (v, std, n)

    # Write file
    path = os.path.join(base.DIR_DATA_OUT, filename)
    print(f'Writing to {os.path.relpath(path)}')
    with open(path, 'w') as f:
        csv = base.csv_writer(f)
        csv.writerow(['x', 'sum', 'gauss'] + fields)
        data = [iter(x), iter(y), iter(z)] + [iter(pdfs[f]) for f in fields]
        for i in range(len(x)):
            csv.writerow([next(j) for j in data])
'''


def midpoints_reports(con):
    """
    Writes a file with the midpoints, SEM, and STD of all reports, ordered by
    Vi where possible, else Va.
    """

    # Gather data
    c = con.cursor()
    q = ('select * from midpoints_wt'
         ' where ni > 0 order by vi')
    r1 = [row for row in c.execute(q)]
    n1 = len(r1)
    q = ('select * from midpoints_wt'
         ' where ni < 1 and na > 0 order by va')
    r2 = [row for row in c.execute(q)]
    n2 = len(r2)

    # Combine
    rows = []
    i1 = i2 = 0
    next_va = r1[i1]['va'] if r1[i1]['na'] > 0 else -1000
    while i1 < n1 and i2 < n2:
        if r2[i2]['va'] < next_va:
            rows.append(r2[i2])
            i2 += 1
        else:
            rows.append(r1[i1])
            i1 += 1
            if i1 < n1 and r1[i1]['na'] > 0:
                next_va = r1[i1]['va']
    for i in range(i1, n1):
        rows.append(r1[i])
    for i in range(i2, n2):
        rows.append(r2[i])

    # Write
    filename = os.path.join(base.DIR_DATA_OUT, 'midpoints-reports.csv')
    print(f'Writing {filename}')
    with open(filename, 'w') as f:
        csv = base.csv_writer(f)
        csv.writerow(['order', 'pub',
                      'va_sem', '+-', 'va_std', '+-',
                      'vi_sem', '+-', 'vi_std', '+-'])
        for k, r in enumerate(rows):
            print(r['pub'])
            row = [k, r['pub']] + ['nan'] * 8
            if r['na'] > 0:
                row[2] = row[4] = r['va']
                row[3] = r['sema']
                row[5] = r['stda']
            if r['ni'] > 0:
                row[6] = row[8] = r['vi']
                row[7] = r['semi']
                row[9] = r['stdi']
            csv.writerow(row)



with base.connect() as con:
    midpoints_reports(con)

