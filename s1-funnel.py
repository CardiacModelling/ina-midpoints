#!/usr/bin/env python3
#
# Supplementary figure 1: Correlation between Va and Vi and experiment size
#
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import base


# Gather data
print('Gathering data')
with base.connect() as con:
    c = con.cursor()

    q = ('select vi, ni from midpoints_wt'
         ' where ni > 0 order by vi')
    r = [row for row in c.execute(q)]
    vi = np.array([x[0] for x in r])
    ni = np.array([x[1] for x in r])

    q = ('select va, na from midpoints_wt'
         ' where na > 0 order by va')
    r = [row for row in c.execute(q)]
    va = np.array([x[0] for x in r])
    na = np.array([x[1] for x in r])
    del(c, q, r)

#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(9, 4.6))    # Two column size
fig.subplots_adjust(0.08, 0.10, 0.97, 0.98, hspace=0.4, wspace=0.3)

grid = fig.add_gridspec(1, 2)

# Va vs study size
vline = dict(color='#999999', ls='--')
ax00 = fig.add_subplot(grid[0, 0])
ax00.set_xlabel('$V_i$ (mV)')
ax00.set_ylabel(r'Experiment size ($\sqrt{n_i}$)')
ax00.axvline(np.mean(vi), **vline)
ax00.plot(vi, np.sqrt(ni), 'o', markerfacecolor='none',
          markeredgecolor='tab:orange')

# Distance to line
ax01 = fig.add_subplot(grid[0, 1])
ax01.set_xlabel('$V_a$ (mV)')
ax01.set_ylabel(r'Experiment size ($\sqrt{n_a}$)')
ax01.axvline(np.mean(va), **vline)
ax01.axvline(np.mean(va), **vline)
ax01.plot(va, np.sqrt(na), 'o', markerfacecolor='none',
          markeredgecolor='tab:blue')

#base.axletter(ax00, 'A', offset=-0.085)
#base.axletter(ax01, 'B', offset=-0.085)

fname = 's1-funnel.png'
print(f'Saving to {fname}')
fig.savefig(fname)
