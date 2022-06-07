#!/usr/bin/env python3
#
# Figure 4: Correlation between Va and Vi
#
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import base


# Gather data
print('Gathering data')
with base.connect() as con:
    c = con.cursor()

    # Get all data
    def get(query):
        """ Return rows of [pub, va, vi, stda, stdi, na, ni]. """
        pub, va, vi, stda, stdi, na, ni = [], [], [], [], [], [], []
        for row in c.execute(query):
            pub.append(row['pub'])
            va.append(row['va'])
            vi.append(row['vi'])
            stda.append(row['stda'])
            stdi.append(row['stdi'])
            na.append(row['na'])
            ni.append(row['ni'])
        return pub, va, vi, stda, stdi, na, ni

    # Get all data, plus data split into biggest subset and rest
    q = ('select pub, va, stda, vi, stdi, na, ni from midpoints_wt'
         ' where (stda != 0 AND stdi != 0)')
    d_all = get(q)
    w = 'sequence == "astar" and beta1 == "yes" and cell == "HEK"'
    d_big = get(q + ' and (' + w + ')')
    w = ('sequence != "astar" or beta1 != "yes" or cell != "HEK"'
         ' or sequence is null or beta1 is null or cell is null')
    d_not = get(q + ' and (' + w + ')')


# Fit line
va, vi = d_all[1], d_all[2]
p1 = np.corrcoef(va, vi)[1, 0]
b1, a1 = np.polyfit(va, vi, 1)
print('Fit to all data')
print(f'  a, b: {a1}, {b1}')
print(f'  Pearson correlation coefficient: {p1}')

va, vi = d_big[1], d_big[2]
p2 = np.corrcoef(va, vi)[1, 0]
b2, a2 = np.polyfit(va, vi, 1)
print(f'Fit to biggest subgroup')
print(f'  a, b: {a2}, {b2}')
print(f'  Pearson correlation coefficient: {p2}')

#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(9, 4.6))    # Two column size
fig.subplots_adjust(0.08, 0.10, 0.97, 0.98, hspace=0.4)

grid = fig.add_gridspec(2, 2)

ax = fig.add_subplot(grid[:, 0])
ax.set_xlabel('$V_a$ (mV)')
ax.set_ylabel('$V_i$ (mV)')
ax.grid(True, ls=':')
xlim = np.array([-70, -10])
ax.set_xlim(*xlim)
ax.set_ylim(-120, -50)

# Ellipses
for va, vi, stda, stdi in zip(*d_all[1:5]):
    e = matplotlib.patches.Ellipse(
        (va, vi), width=4*stda, height=4*stdi,
        facecolor='blue', edgecolor='k', alpha=0.05)
    ax.add_artist(e)

# Projections / orthogonal
a, b = a1, b1

# Mean x and y, projected onto line (should pretty much equal the mean)
va, vi = np.mean(d_all[1]), np.mean(d_all[2])
f = (va + (vi - a) * b) / (1 + b * b)
mx, my = f, a + f * b

# Project all points onto fit, then get tangential and orthogonal length
d1s, d2s = [], []
for va, vi in zip(d_all[1], d_all[2]):
    f = (va + (vi - a) * b) / (1 + b * b)
    x, y = f, a + f * b

    d1 = np.sqrt((va - x)**2 + (vi - y)**2)
    d2 = np.sqrt((mx - x)**2 + (my - y)**2)

    d1 *= (1 if vi > y else -1)
    d2 *= (1 if x > mx else -1)

    ax.plot((va, x), (vi, y), color='#999999', lw=1)
    #ax.plot((mx, x), (my, y), color='k', zorder=20)

    d1s.append(d1)
    d2s.append(d2)
d1s, d2s = np.array(d1s), np.array(d2s)

# Linear fit
l1 = ax.plot(xlim, a1 + b1 * xlim, '-', color='tab:pink',
             label=f'{a1:.2f} mV + {b1:.2f} $V_a$')
#l2 = ax.plot(xlim, a2 + b2 * xlim, '--', color='tab:brown', label='Fit to subgroup')

# Midpoints
m = 'o'
ax.plot(d_not[1], d_not[2], m, color='k', markerfacecolor='w')
ax.plot(d_big[1], d_big[2], m, color='k')

# Custom legend
ms2 = 12
elements = [
    matplotlib.lines.Line2D([0], [0], marker=m, color='k', ls='none',
                            label=r'a*, ${\beta}1$, HEK'),
    matplotlib.lines.Line2D([0], [0], marker=m, color='k', ls='none',
                            markerfacecolor='w', label='Other'),
    matplotlib.lines.Line2D([0], [0], marker=m, color='b', ls='none',
                            label=r'$2\sigma$ range'),
    l1[0],
#    l2[0],
]
ax.legend(loc='lower right', handles=elements, framealpha=1)


# Distance along line
grey = '#bbbbbb'
xlim2 = -35, 35
ax01 = fig.add_subplot(grid[0, 1])
ax01.set_xlabel('Distance to best fit line (mV)')
ax01.set_xlim(*xlim2)
for s in ax01.spines.values():
    s.set_visible(False)
ax01.spines['bottom'].set_visible(True)
ax01.get_yaxis().set_visible(False)
ax01.hist(d1s, ec='k', fc=grey)

# Distance to line
ax11 = fig.add_subplot(grid[1, 1])
ax11.set_xlabel('Distance along best fit line (mV)')
ax11.set_xlim(*xlim2)
for s in ax11.spines.values():
    s.set_visible(False)
ax11.spines['bottom'].set_visible(True)
ax11.get_yaxis().set_visible(False)
ax11.hist(d2s, ec='k', fc=grey)

base.axletter(ax, 'A', offset=-0.07, tweak=0.01)
base.axletter(ax01, 'B', tweak=0.01)
base.axletter(ax11, 'C')

fname = 'f4-correlation.pdf'
print(f'Saving to {fname}')
fig.savefig(fname)


#
# Versus n
#
print('Creating figure')
fig = plt.figure(figsize=(9, 4.6))    # Two column size
fig.subplots_adjust(0.08, 0.10, 0.97, 0.98, hspace=0.4)

ax = fig.add_subplot(1, 2, 1)
ax.set_xlabel('Study size ($\sqrt{n_a + n_i}$)')
ax.set_ylabel('Distance to best fit line')
na, ni = np.array(d_all[5]), np.array(d_all[6])
ax.plot(np.sqrt(na + ni), d1s, 'o')

ax = fig.add_subplot(1, 2, 2)
ax.set_xlabel('Study size ($\sqrt{n_a + n_i}$)')
ax.set_ylabel('Distance along best fit line')
na, ni = np.array(na), np.array(ni)
ax.plot(np.sqrt(na + ni), d2s, 'o')


fname = 'f5-study-size.pdf'
print(f'Saving to {fname}')
fig.savefig(fname)

