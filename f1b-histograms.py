#!/usr/bin/env python3
#
# Figure 1: All data, as histograms
#
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import base

# Sigma multiplier to get 90-th percentile
# Find as -scipy.stats.norm.ppf(0.05)
s90 = 1.6448536269514729
top90 = lambda sigma: sigma * s90 * 2
frp90 = lambda p90: p90 / (s90 * 2)

# Gather data
print('Gathering data')
with base.connect() as con:
    c = con.cursor()

    q = ('select vi, stdi from midpoints_wt'
         ' where ni > 0 order by vi')
    vi, stdi = np.array([row for row in c.execute(q)]).T
    q = ('select va, stda from midpoints_wt'
         ' where na > 0 order by va')
    va, stda = np.array([row for row in c.execute(q)]).T


#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(4.2, 4))    # One column size
fig.subplots_adjust(0.12, 0.11, 0.97, 0.99, wspace=0.05, hspace=0.85)
grid = fig.add_gridspec(2, 2)

bins = np.arange(-110, -10, 2.5)
kwargs = dict(bins=bins, facecolor='none')
ax1 = fig.add_subplot(grid[0, :])
ax1.set_xlabel('Membrane potential (mV)')
ax1.set_ylabel('Percentage')
ax1.set_xlim(-112, -18)

w = np.ones(len(vi)) / len(vi) * 100
ax1.hist(vi, weights=w, edgecolor='tab:orange', **kwargs)
w = np.ones(len(va)) / len(va) * 100
ax1.hist(va, weights=w, edgecolor='tab:blue', **kwargs)

bins = np.arange(0, 24, 1)
kwargs = dict(bins=bins, facecolor='none', cumulative=True)
xlim = -1, 24
ylim = 0, 101

ax2 = fig.add_subplot(grid[1, :])
ax2.set_xlabel('$\sigma$ (mV)')
ax2.set_ylabel('Percentage')
ax2x = ax2.secondary_xaxis('top', functions=(top90, frp90))
ax2x.set_xlabel('90th percentile (mV)')
ax2.set_xlim(*xlim)
ax2.set_ylim(*ylim)

for p in [25, 50, 75]:
    ax2.axhline(p, ls='--', lw=1, color='#bbb', zorder=-1)

w = np.ones(len(stdi)) / len(stdi) * 100
ax2.hist(stdi, weights=w, edgecolor='tab:orange', **kwargs)
w = np.ones(len(stda)) / len(stda) * 100
ax2.hist(stda, weights=w, edgecolor='tab:blue', **kwargs)

fname = 'f1b-hist.pdf'
print(f'Saving to {fname}')
fig.savefig(fname)
