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
    q = ('select vi, semi, stdi, ni from midpoints_wt'
         f' where ni > 0 {qand} order by vi')
    i = [row for row in c.execute(q)]
    q = ('select va, sema, stda, na from midpoints_wt'
         f' where na > 0 {qand} order by va')
    a = [row for row in c.execute(q)]

#
# Create figure
#
print('Creating figure')
#fig = plt.figure(figsize=(9, 7.5))    # Two column size
#fig.subplots_adjust(0.058, 0.06, 0.99, 0.99, hspace=0.3)
#grid = fig.add_gridspec(2, 2, height_ratios=[4.5, 1])
fig = plt.figure(figsize=(9, 10.5))    # Two column size
fig.subplots_adjust(0.054, 0.04, 0.987, 0.995, hspace=0.3)

grid1 = fig.add_gridspec(2, 1, height_ratios=[3.1, 1], hspace=0.12)
grid2 = grid1[1, 0].subgridspec(2, 2, hspace=1.25)

ax1 = fig.add_subplot(grid1[0, :])
ax21 = fig.add_subplot(grid2[0, :])
ax31 = fig.add_subplot(grid2[1, 0])
ax32 = fig.add_subplot(grid2[1, 1])


#
# Top: all data
#
xlim = -120, 0
ax1.set_xlabel('Membrane potential (mV)')
ax1.set_xlim(*xlim)
ax1.set_ylim(-2, 1 + max(len(a), len(i)))
for s in ax1.spines.values():
    s.set_visible(False)
ax1.spines['bottom'].set_visible(True)
ax1.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(20))
ax1.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
ax1.get_yaxis().set_visible(False)
ax1.grid(ls='--', color='#cccccc', zorder=0)

sstd = dict(color='#999')
ssem = dict(color='k', lw=3)
ca = 'tab:blue'
ci = 'tab:orange'
m = 'o'
ms = 3

offset = max(0, (len(a) - len(i)) / 2)
for k, d in enumerate(i):
    mu, sem, std, n = d

    k += offset
    ax1.plot((mu - s90 * std, mu + s90 * std), (k, k), **sstd, zorder=2)
    ax1.plot((mu - sem, mu + sem), (k, k), **ssem, zorder=3)
    ax1.plot(mu, k, m, color=ci, markersize=ms, zorder=4)

offset = max(0, (len(i) - len(a)) / 2)
for k, d in enumerate(a):
    mu, sem, std, n = d

    ax1.plot((mu - s90 * std, mu + s90 * std), (k, k), **sstd, zorder=2)
    ax1.plot((mu - sem, mu + sem), (k, k), **ssem, zorder=3)
    ax1.plot(mu, k, m, color=ca, markersize=ms, zorder=4)

ms2 = 12
elements = [
    matplotlib.lines.Line2D([0], [0], marker=m, color='w', label=r'$\mu_i$',
                            markersize=ms2, markerfacecolor=ci),
    matplotlib.lines.Line2D([0], [0], marker=m, color='w', label=r'$\mu_a$',
                            markersize=ms2, markerfacecolor=ca),
    matplotlib.lines.Line2D([0], [0], color=ssem['color'], label='SEM',
                            lw=ssem['lw']),
    matplotlib.lines.Line2D([0], [0], color=sstd['color'],
                            label='5th-95th percentile'),
]
ax1.legend(loc='upper left', frameon=False, handles=elements)

#
# Middle: histogram of Vi, Va
#
vi, _, stdi, ni = np.array([row for row in i]).T
va, _, stda, na = np.array([row for row in a]).T

bins = np.arange(*xlim, 2.5)
kwargs = dict(bins=bins, facecolor='none')
ax21.set_xlabel('Membrane potential (mV)')
ax21.set_ylabel('Percentage')
ax21.set_xlim(*xlim)

w = np.ones(len(vi)) / len(vi) * 100
ax21.hist(vi, weights=w, edgecolor='tab:orange', label=r'$\mu_i$', **kwargs)
w = np.ones(len(va)) / len(va) * 100
ax21.hist(va, weights=w, edgecolor='tab:blue', label=r'$\mu_a$', **kwargs)
ax21.legend(loc='upper left', frameon=False)

#
# Bottom: Histogram of sigma and of n
#
ax31.set_xlabel(r'$\sigma$ (mV)')
ax31.set_ylabel('Percentage')
ax31.set_xlim(-1, 24)
ax31.set_ylim(0, 23)
top90 = lambda sigma: sigma * s90 * 2
frp90 = lambda p90: p90 / (s90 * 2)
ax31t = ax31.secondary_xaxis('top', functions=(top90, frp90))
ax31t.set_xlabel('5th-95th percentile range (mV)')

bins = np.arange(0, 24, 1)
kwargs = dict(bins=bins, facecolor='none')
w = np.ones(len(stdi)) / len(stdi) * 100
ax31.hist(stdi, weights=w, edgecolor='tab:orange', label=r'$\sigma_i$',
          **kwargs)
w = np.ones(len(stda)) / len(stda) * 100
ax31.hist(stda, weights=w, edgecolor='tab:blue', label=r'$\sigma_a$', **kwargs)
ax31.legend(loc='upper right', frameon=False)

ax32.set_xlabel('n')
ax32.set_ylabel('Percentage')
ax32.set_xlim(1, 90)

bins = np.arange(1, 90, 2)
kwargs = dict(bins=bins, facecolor='none')
w = np.ones(len(stdi)) / len(stdi) * 100
ax32.hist(ni, weights=w, edgecolor='tab:orange', label=r'$n_i$', **kwargs)
w = np.ones(len(stda)) / len(stda) * 100
ax32.hist(na, weights=w, edgecolor='tab:blue', label=r'$n_a$', **kwargs)
ax32.legend(loc='upper right', frameon=False)
print(min(na), min(ni))
print(max(na), max(ni))

#
# Save
x = -0.045
#
y = 0.025
base.axletter(ax1, 'A', offset=x)
base.axletter(ax21, 'B', offset=x, tweak=y)
base.axletter(ax31, 'C', offset=x, tweak=y)
base.axletter(ax32, 'D', offset=x, tweak=y)

fname = 'f2-all' + ('.png' if 'png' in sys.argv else '.pdf')
print(f'Saving to {fname}')
fig.savefig(fname, dpi=300)
