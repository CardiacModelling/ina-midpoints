#!/usr/bin/env python3
#
# Figure 1: All data
#
import matplotlib
import matplotlib.pyplot as plt

import base


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
fig = plt.figure(figsize=(6, 6))    # Two-third column size
fig.subplots_adjust(0.04, 0.075, 0.99, 0.99)

ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Membrane potential (mV)')
ax.set_xlim(-120, 0)
ax.set_ylim(-2, 187)
for s in ax.spines.values():
    s.set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(20))
ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
ax.get_yaxis().set_visible(False)
ax.grid(ls='--', color='#cccccc', zorder=0)

sstd = dict(color='#888888')
ssem = dict(color='k', lw=3)
ca = 'tab:blue'
ci = 'tab:orange'
m = 'o'
ms = 3

offset = max(0, (len(a) - len(i)) / 2)
for k, d in enumerate(i):
    mu, sem, std = d

    k += offset
    ax.plot((mu - 2 * std, mu + 2 * std), (k, k), **sstd, zorder=2)
    ax.plot((mu - sem, mu + sem), (k, k), **ssem, zorder=3)
    ax.plot(mu, k, m, color=ci, markersize=ms, zorder=4)

offset = max(0, (len(i) - len(a)) / 2)
for k, d in enumerate(a):
    mu, sem, std = d

    ax.plot((mu - 2 * std, mu + 2 * std), (k, k), **sstd, zorder=2)
    ax.plot((mu - sem, mu + sem), (k, k), **ssem, zorder=3)
    ax.plot(mu, k, m, color=ca, markersize=ms, zorder=4)

ms2 = 12
elements = [
    matplotlib.lines.Line2D([0], [0], marker=m, color='w', label='$V_i$',
                            markersize=ms2, markerfacecolor=ci),
    matplotlib.lines.Line2D([0], [0], marker=m, color='w', label='$V_a$',
                            markersize=ms2, markerfacecolor=ca),
    matplotlib.lines.Line2D([0], [0], color=ssem['color'], label='SEM',
                            lw=ssem['lw']),
    matplotlib.lines.Line2D([0], [0], color=sstd['color'], label='STD'),
]
ax.legend(loc='upper left', frameon=False, handles=elements)

fname = 'f1-all.pdf'
print(f'Saving to {fname}')
fig.savefig(fname)
