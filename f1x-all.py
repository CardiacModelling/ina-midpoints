#!/usr/bin/env python3
#
# Figure 1: All data, sorted from low to high, no correlations
#
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import base

# Sigma multiplier to get 90-th percentile
# Find as -scipy.stats.norm.ppf(0.05)
s90 = 1.6448536269514729


# Gather data
print('Gathering data')
with base.connect() as con:
    c = con.cursor()

    q = ('select vi, semi, stdi from midpoints_wt'
         ' where ni > 0 order by vi')
    i = [row for row in c.execute(q)]
    q = ('select va, sema, stda from midpoints_wt'
         ' where na > 0 order by va')
    a = [row for row in c.execute(q)]


#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(9, 8))    # Two column size
fig.subplots_adjust(0.056, 0.054, 0.99, 0.99, hspace=0.3, wspace=0.4)
grid = fig.add_gridspec(2, 3, height_ratios=[5, 1])

#
# Top: all data
#
ax1 = fig.add_subplot(grid[0, :])
ax1.set_xlabel('Membrane potential (mV)')
ax1.set_xlim(-120, 0)
ax1.set_ylim(-2, 187)
for s in ax1.spines.values():
    s.set_visible(False)
ax1.spines['bottom'].set_visible(True)
ax1.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(20))
ax1.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
ax1.get_yaxis().set_visible(False)
ax1.grid(ls='--', color='#cccccc', zorder=0)

sstd = dict(color='k', alpha=0.4, rasterized=True)
ssem = dict(color='k', lw=3)
ca = 'tab:blue'
ci = 'tab:orange'
m = 'o'
ms = 3

offset = max(0, (len(a) - len(i)) / 2)
for k, d in enumerate(i):
    mu, sem, std = d

    k += offset
    ax1.plot((mu - s90 * std, mu + s90 * std), (k, k), **sstd, zorder=2)
    ax1.plot((mu - sem, mu + sem), (k, k), **ssem, zorder=3)
    ax1.plot(mu, k, m, color=ci, markersize=ms, zorder=4)

offset = max(0, (len(i) - len(a)) / 2)
for k, d in enumerate(a):
    mu, sem, std = d

    ax1.plot((mu - s90 * std, mu + s90 * std), (k, k), **sstd, zorder=2)
    ax1.plot((mu - sem, mu + sem), (k, k), **ssem, zorder=3)
    ax1.plot(mu, k, m, color=ca, markersize=ms, zorder=4)

ms2 = 12
elements = [
    matplotlib.lines.Line2D([0], [0], marker=m, color='w', label='$\mu_i$',
                            markersize=ms2, markerfacecolor=ci),
    matplotlib.lines.Line2D([0], [0], marker=m, color='w', label='$\mu_a$',
                            markersize=ms2, markerfacecolor=ca),
    matplotlib.lines.Line2D([0], [0], color=ssem['color'], label='SEM',
                            lw=ssem['lw']),
    matplotlib.lines.Line2D([0], [0], color=sstd['color'],
        label='90th percentile'),
]
ax1.legend(loc='upper left', frameon=False, handles=elements)

#
# Bottom: histograms
#
vi, _, stdi = np.array([row for row in i]).T
va, _, stda = np.array([row for row in a]).T

bins = np.arange(-110, -10, 2.5)
kw1 = dict(bins=bins, facecolor='none')
lw = dict(frameon=False, handlelength=0.4, handletextpad=0.4,
          borderaxespad=0.1)
xlim1 = -112, -18
wvi = np.ones(len(vi)) / len(vi) * 100
wva = np.ones(len(va)) / len(va) * 100

ax21 = fig.add_subplot(grid[1, 0])
ax21.set_xlabel('Membrane potential (mV)')
ax21.set_ylabel('Percentage')
ax21.set_xlim(*xlim1)
ax21.hist(vi, weights=wvi, edgecolor='tab:orange', label='$\mu_i$', **kw1)
ax21.hist(va, weights=wva, edgecolor='tab:blue', label='$\mu_a$', **kw1)
ax21.legend(loc='upper left', **lw)

bins = np.arange(0, 24, 1)
kw2 = dict(bins=bins, facecolor='none')
xlim2 = -1, 24
ylim2 = 0, 22

ax22 = fig.add_subplot(grid[1, 1])
ax22.set_xlabel('$\sigma$ (mV)')
ax22.set_ylabel('Percentage')
ax22.set_xlim(*xlim2)
ax22.set_ylim(*ylim2)
top90 = lambda sigma: sigma * s90 * 2
frp90 = lambda p90: p90 / (s90 * 2)
ax22t = ax22.secondary_xaxis('top', functions=(top90, frp90))
ax22t.set_xlabel('90th percentile (mV)')

wsi = np.ones(len(stdi)) / len(stdi) * 100
wsa = np.ones(len(stda)) / len(stda) * 100
ax22.hist(stdi, weights=wsi, edgecolor='tab:orange', label='$\sigma_i$', **kw2)
ax22.hist(stda, weights=wsa, edgecolor='tab:blue', label='$\sigma_a$', **kw2)
ax22.legend(loc='upper right', **lw)

#
# Cumulative
#
kw2['cumulative'] = True
ax23 = fig.add_subplot(grid[1, 2])
ax23.set_xlabel('$\sigma$ (mV)')
ax23.set_ylabel('Cumulative %')
ax23.set_yticks((0, 25, 50, 75, 100))
ax23.set_xlim(*xlim2)
ax23t = ax23.secondary_xaxis('top', functions=(top90, frp90))
ax23t.set_xlabel('90th percentile (mV)')
ax23.hist(stdi, weights=wsi, edgecolor='tab:orange', label='$\sigma_i$', **kw2)
ax23.hist(stda, weights=wsa, edgecolor='tab:blue', label='$\sigma_a$', **kw2)
ax23.legend(loc='upper left', **lw)
for p in (25, 50, 75):
    ax23.axhline(p, ls='--', lw=1, color='#bbb', zorder=-1)


#
# Save
#

x = -0.045
y = 0.025
base.axletter(ax1, 'A', offset=x)
base.axletter(ax21, 'B', offset=x, tweak=y)
base.axletter(ax22, 'C', tweak=y)

fname = 'f1-all' + ('.png' if 'png' in sys.argv else '.pdf')
print(f'Saving to {fname}')
fig.savefig(fname, dpi=300)
