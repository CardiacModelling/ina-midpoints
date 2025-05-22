#!/usr/bin/env python3
#
# Figure 2: All data, sorted from low to high, no correlations
#
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import base

# Sigma multiplier to get 90-th percentile
s90 = 1.6448536269514729

# Include Oocytes or not
nooocytes = True

# Gather data
print('Gathering data')
with base.connect() as con:
    c = con.cursor()

    qand = ' and cell != "Oocyte"' if nooocytes else ''
    q = f'select stdi, ni from midpoints_wt where ni > 0 {qand}'
    si, ni = [], []
    for r in c.execute(q):
        si.append(r[0])
        ni.append(r[1])

    q = (f'select stda, na from midpoints_wt where na > 0 {qand} order by va')
    sa, na = [], []
    for r in c.execute(q):
        sa.append(r[0])
        na.append(r[1])

#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(4, 4))
fig.subplots_adjust(0.125, 0.11, 0.99, 0.99)

kwargs = dict(markerfacecolor='none')
ax = fig.add_subplot()
ax.set_xlabel('sample size (n)')
ax.set_ylabel('sample standard deviation ($\sigma$)')
ax.plot(ni, si, 'o', label=r'$\sigma_i$', **kwargs)
ax.plot(na, sa, 'o', label=r'$\sigma_a$', **kwargs)
ax.legend(loc='upper right')

#
# Save
#
fname = 'x1-sigma-vs-n' + ('.png' if 'png' in sys.argv else '.pdf')
print(f'Saving to {fname}')
fig.savefig(fname, dpi=300)
