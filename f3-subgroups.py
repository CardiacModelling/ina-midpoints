#!/usr/bin/env python3
#
# Figure 3: Highlighted subgroups
#
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


#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(9, 4))    # Two column size
fig.subplots_adjust(0.04, 0.045, 0.99, 0.99, hspace=0.2)

grid = fig.add_gridspec(3, 1)

c1 = 'tab:orange'
c2 = 'tab:red'

ax = fig.add_subplot(grid[:, 0])
ax.set_xlabel('$V_a$ (mV)')
ax.set_ylabel('$V_i$ (mV)')
ax.grid(True, ls=':')
xlim = np.array([-70, -10])
ax.set_xlim(*xlim)
ax.set_ylim(-120, -50)






def format_axes(ax):
    ax.set_xlabel('Membrane potential (mV)')
    ax.set_xlim(-120, 0)
    ax.set_ylim(-2, 187)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(40))
    ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
    ax.get_yaxis().set_visible(False)


def el(label=None, marker=None, markersize=None, color=None,
       markerfacecolor=None, markeredgecolor=None, lw=None):
    lw = {} if lw is None else {'lw': lw}
    return matplotlib.lines.Line2D(
        [0],
        [0],
        label=label,
        marker=marker,
        markersize=markersize,
        color=color,
        markerfacecolor=markerfacecolor,
        markeredgecolor=markeredgecolor,
        **lw
    )


def plot(ax, label, f, marker='o', letter=None):

    sstd = dict(color='#bbbbbb')
    #ssem = dict(color='k', lw=3)
    m1 = dict(zorder=3, markersize=3, marker='o', color='tab:orange')
    m2 = dict(zorder=4, markersize=5, marker=marker,
              markeredgecolor='k', markerfacecolor='w')

    m1['color'] = 'tab:orange'
    offset = max(0, (len(a) - len(i)) / 2)
    for k, d in enumerate(i):
        k += offset
        mu, sem, std, seq, bet, cell = d
        m = m2 if f(seq, bet, cell) else m1
        ax.plot((mu - 2 * std, mu + 2 * std), (k, k), **sstd, zorder=1)
        #ax.plot((mu - sem, mu + sem), (k, k), **ssem, zorder=2)
        ax.plot(mu, k, **m)

    m1['color'] = 'tab:blue'
    offset = max(0, (len(i) - len(a)) / 2)
    for k, d in enumerate(a):
        k += offset
        mu, sem, std, seq, bet, cell = d
        m = m2 if f(seq, bet, cell) else m1
        ax.plot((mu - 2 * std, mu + 2 * std), (k, k), **sstd, zorder=1)
        #ax.plot((mu - sem, mu + sem), (k, k), **ssem, zorder=2)
        ax.plot(mu, k, **m)

    ms2 = 12
    els = [
        el(label, marker, ms2, markeredgecolor='k', markerfacecolor='w', lw=0),
    ]
    ax.legend(loc=(-0.15, 0.87), frameon=False, handlelength=1, handles=els)
    if letter:
        base.axletter(ax, letter, offset=-0.0175)


#
# Alpha subunit
#
ax = fig.add_subplot(2, 4, 1)
format_axes(ax)
plot(ax, 'a', lambda seq, bet, cell: seq == 'a', letter='A')

ax = fig.add_subplot(2, 4, 2)
format_axes(ax)
plot(ax, 'a*', lambda seq, bet, cell: seq == 'astar')

ax = fig.add_subplot(2, 4, 3)
format_axes(ax)
plot(ax, 'b', lambda seq, bet, cell: seq == 'b')

ax = fig.add_subplot(2, 4, 4)
format_axes(ax)
plot(ax, 'b*', lambda seq, bet, cell: seq == 'bstar')

ax = fig.add_subplot(2, 4, 5)
format_axes(ax)
plot(ax, r'With $\beta1$', lambda seq, bet, cell: bet == 'yes', letter='B',
     marker='s')

ax = fig.add_subplot(2, 4, 6)
format_axes(ax)
plot(ax, 'CHO', lambda seq, bet, cell: cell == 'CHO', marker='^', letter='C')

ax = fig.add_subplot(2, 4, 7)
format_axes(ax)
plot(ax, 'Oocyte', lambda seq, bet, cell: cell == 'Oocyte', marker='^')

ax = fig.add_subplot(2, 4, 8)
format_axes(ax)
plot(ax, 'a*, $\\beta1$,HEK',
     lambda seq, bet, cell: seq == 'astar' and bet == 'yes' and cell == 'HEK',
     letter='D')

fname = 'f3-subgroups.pdf'
print(f'Saving to {fname}')
fig.savefig(fname)
