#!/usr/bin/env python3
#
# Figure 4: Correlation between Va and Vi
#
import os

import matplotlib
import matplotlib.pyplot as plt

import base


# Gather data
print('Gathering data')
with base.connect() as con:
    c = con.cursor()


    q = ('select vi, semi, stdi, sequence, beta1, cell from midpoints_wt'
         ' where ni > 0 order by vi')
    i = [row for row in c.execute(q)]
    q = ('select va, sema, stda, sequence, beta1, cell from midpoints_wt'
         ' where na > 0 order by va')
    a = [row for row in c.execute(q)]



def gather(query, filename1, filename2):
    """
    Queries the DB for reports of both activation and inactivation and does
    some analysis:

    1. Writes a CSV file containing the midpoints plus 2 sigma intervals.
    2. Fits a linear regression line.
    3. Writes a 2nd CSV file containing the midpoints minus the regression.
    row.
    4. Creates and returns a table row.

    The returned row contains the fields ``(nreports, a, b, p, sd_diff)``,
    where ``nreports`` is the number of reports used, ``a`` and ``b`` are the
    regression offset and slope, ``p`` is the Pearson correlation coefficient,
    and ``sd_diff`` is the standard deviation of ``V_a - V_i``.
    """
    # Query db
    data = []
    with base.connect() as con:
        c = con.cursor()
        for row in c.execute(query):
            data.append((
                row['pub'],
                row['va'],
                row['stda'] * 2,
                row['vi'],
                row['stdi'] * 2,
                row['va'] - row['vi'],
            ))

    # Write first file
    path = os.path.join(base.DIR_DATA_OUT, filename1)
    print(f'Writing to {os.path.relpath(path)}')
    with open(path, 'w') as f:
        csv = base.csv_writer(f)
        csv.writerow(['pub', 'va', '+-', 'vi', '+-', 'dv'])
        for row in data:
            csv.writerow(row)

    #
    # Correct with linear regression
    #
    # Gather data
    va = []
    vi = []
    for row in data:
        va.append(row[1])
        vi.append(row[3])
    va = np.array(va)
    vi = np.array(vi)

    # Fit line
    b, a = np.polyfit(va, vi, 1)

    # Subtract and write to file
    path = os.path.join(base.DIR_DATA_OUT, filename2)
    print(f'Writing to {os.path.relpath(path)}')
    with open(path, 'w') as f:
        csv = base.csv_writer(f)
        csv.writerow(['pub', 'va', '+-', 'vic', '+-'])
        for k, row in enumerate(data):
            row = list(row[:-1])
            row[3] = row[3] - (a + b * row[1])
            csv.writerow(row)

    # Get Pearson correlation coefficient
    p = np.corrcoef(va, vi)[1, 0]

    # Get standard deviation of Va - Vi
    sd_diff = np.std(va - vi)

    # Return row
    return [len(data), a, b, p, sd_diff]




'''
    head = ['', 'reports', 'a', 'b', 'Pearson', 'Sigma Va-Vi']
    rows = []

    # All data
    q = 'select pub, va, stda, vi, stdi from midpoints_wt'
    q += ' where va != 0'
    q += ' AND vi != 0'
    q += ' AND stda != 0'
    q += ' AND stdi != 0'
    fname1 = 'midpoint-correlations.csv'
    fname2 = 'midpoint-correlations-regression.csv'
    rows.append(['All'] + gather(q, fname1, fname2))

    # Largest subgroup
    q += ' and sequence == "astar"'
    q += ' and cell == "HEK"'
    q += ' and beta1 == "yes"'
    fname1 = 'midpoint-correlations-largest-subgroup.csv'
    fname2 = 'midpoint-correlations-regression-largest-subgroup.csv'
    rows.append(['Most common'] + gather(q, fname1, fname2))

    print()
    base.table(head, rows)
'''


#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(6, 6))    # Two-third column size
fig.subplots_adjust(0.04, 0.075, 0.99, 0.99)

ax = fig.add_subplot(1, 1, 1)


fname = 'f4-correlation.pdf'
print(f'Saving to {fname}')
fig.savefig(fname)
