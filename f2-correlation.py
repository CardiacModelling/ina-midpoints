#!/usr/bin/env python3
#
# Figure 2: Correlation between Va and Vi
#
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import base

# Sigma multiplier to get 90-th percentile
# Find as -scipy.stats.norm.ppf(0.05)
s90 = 1.6448536269514729

# Include oocytes
nooocytes = True

# Plot tweaks
highlight_example = True
#iexample = 72 if nooocytes else 82
iexample = 15 if nooocytes else 16

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

    qand = 'and cell != "Oocyte"' if nooocytes else ''
    q = ('select pub, va, stda, vi, stdi, na, ni from midpoints_wt'
         f' where (na > 0 and ni > 0 {qand})')
    d_all = get(q)
    n_all = len(d_all[0])

# Extract va and vi
va, vi = np.array(d_all[1]), np.array(d_all[2])

# Find example point
i = np.where(va < -55)[0]
i = i[np.where(vi[i] > -100)[0]]
#print(i, va[i], vi[i])

# Fit line
p1 = np.corrcoef(va, vi)[1, 0]
b1, a1 = np.polyfit(va, vi, 1)
print('Fit to all data')
print(f'  a, b: {a1}, {b1}')
print(f'  Pearson correlation coefficient: {p1}')
mu_a, mu_i = np.mean(va), np.mean(vi)
print('Mean:')
print(f'  {mu_a}')
print(f'  {mu_i}')

# Fit line with slope of 1
a2 = np.polyfit(va, vi - va, 0)[0]
b2 = 1
print('Slope=1 fit')
print(f'  a, b: {a2}, {b2}')

#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(9, 4.35))    # Two column size
fig.subplots_adjust(0.08, 0.11, 0.98, 0.98, hspace=0.4, wspace=0.3)
xlim = -65, -15
ylim = -112, -58
# NOTE: These measurements chosen to get almost equal aspect manually
grid = fig.add_gridspec(2, 2)


c1 = 'tab:orange'
c2 = 'tab:red'

ax = fig.add_subplot(grid[:, 0])
ax.set_xlabel(r'$\mu_a$ (mV)')
ax.set_ylabel(r'$\mu_i$ (mV)')
ax.grid(True, ls=':')
ax.set(xlim=xlim, ylim=ylim)
#ax.axis('equal')  This changes the limits

# Ellipses
for va, vi, stda, stdi in zip(*d_all[1:5]):
    e = matplotlib.patches.Ellipse(
        (va, vi), width=2 * s90 * stda, height=2 * s90 * stdi,
        facecolor='tab:blue', edgecolor='k', alpha=0.05)
    ax.add_artist(e).set_rasterized(True)

# Projections / orthogonal
a, b = a1, b1

# Mean x and y, projected onto line (should stay the same!)
va, vi = np.mean(d_all[1]), np.mean(d_all[2])
f = (va + (vi - a) * b) / (1 + b * b)
mx, my = f, a + f * b

# Project all points onto fit, then get tangential and orthogonal length
va, vi = d_all[1], d_all[2]
d1s = ((va - mx) + b * (vi - my)) / np.sqrt(1 + b**2)
d2s = ((vi - my) - b * (va - mx)) / np.sqrt(1 + b**2)

# Plot linear fit
xlim = np.array(xlim)
l1 = ax.plot(xlim, a1 + b1 * xlim, '-', color='tab:pink',
             label=f'{a1:.1f} mV + {b1:.2f} $V_a$')

# Plot fixed-slope fit
l2 = ax.plot(xlim, a2 + b2 * xlim, '--', color='tab:pink',
             label=f'{a2:.1f} mV + {b2:.2f} $V_a$')

# Plot midpoints
m = 'o'
ax.plot(d_all[1], d_all[2], m, color='k', markerfacecolor='w')
if highlight_example:
    ax.plot(d_all[1][iexample], d_all[2][iexample], m, color='k')
#            markerfacecolor='w', markeredgecolor='k')

# Example decomposition
va, vi = d_all[1][iexample], d_all[2][iexample]
f = (va + (vi - a) * b) / (1 + b * b)
x, y = f, a + f * b
arrow = dict(length_includes_head=True, edgecolor='k',
             width=0.5, head_width=2.0, head_length=2.0, lw=0.5, zorder=3)
ar1 = ax.arrow(mu_a, mu_i, (x - mu_a), (y - mu_i), facecolor=c1, **arrow)
ar2 = ax.arrow(x, y, (va - x), (vi - y), facecolor=c2, **arrow)
print(f'Example point: {va}, {vi}')
print(f'             : {d1s[iexample]}, {d2s[iexample]}')

# Mean
mean = ax.plot(mu_a, mu_i, '*', color='yellow', lw=5, markersize=15,
               markeredgecolor='k', markeredgewidth=1, label='mean', zorder=4)

# Custom legend
def l2d(**kwargs):
    return matplotlib.lines.Line2D([0], [0], **kwargs)

ms2 = 12
elements = [
    l2d(marker=m, color='k', ls='none', markerfacecolor='w',
        label=f'Experiments ({len(d_all[1])})'),
    l2d(marker=m, color='tab:blue', ls='none', label=r'90th percentiles'),
    l2d(marker='*', ls='none', color='yellow', markersize=11,
        markeredgecolor='k', label='Mean-of-means'),
    l1[0],
    l2[0],
]

ax.legend(loc='lower right', handles=elements, framealpha=1 , fontsize=9)

# Principal components vs study size
na, ni = np.array(d_all[5]), np.array(d_all[6])
xlim = -35, 35
vline = dict(color='#999999', ls='--')
ax01 = fig.add_subplot(grid[0, 1])
ax01.set_xlabel('First principal component (mV)')
ax01.set_ylabel(r'Exp. size ($\sqrt{n_a + n_i}$)')
ax01.set_xlim(*xlim)
ax01.axvline(0, **vline)
na, ni = np.array(na), np.array(ni)
ax01.plot(d1s, np.sqrt(na + ni), 'o', markerfacecolor='none',
          markeredgecolor=c1)
if highlight_example:
    print(d1s[iexample])
    ax01.plot(d1s[iexample], np.sqrt(na + ni)[iexample], 'o',
              markerfacecolor='none', markeredgecolor='k')

# Second component
ax11 = fig.add_subplot(grid[1, 1])
ax11.set_xlabel('Second principal component (mV)')
ax11.set_ylabel(r'Exp. size ($\sqrt{n_a + n_i}$)')
ax11.set_xlim(*xlim)
ax11.axvline(0, **vline)
ax11.plot(d2s, np.sqrt(na + ni), 'o', markerfacecolor='none',
          markeredgecolor=c2)
if highlight_example:
    print(d2s[iexample])
    ax11.plot(d2s[iexample], np.sqrt(na + ni)[iexample], 'o',
              markerfacecolor='none', markeredgecolor='k')

base.axletter(ax, 'A', offset=-0.07, tweak=0.01)
base.axletter(ax01, 'B', offset=-0.090)
base.axletter(ax11, 'C', offset=-0.090, tweak=0.01)

if False:
    pubs = {}
    with base.connect() as con:
        q = 'select key, author, year, title, journal from publication'
        for row in con.cursor().execute(q):
            pubs[row['key']] = (f'{row["author"]} ({row["year"]})'
                                f' {row["title"]}; {row["journal"]}')
    n = 3
    i = np.argsort(d1s)
    va, vi = np.array(d_all[1]), np.array(d_all[2])
    ax.plot(va[i[:n]], vi[i[:n]], 'kx')
    va, vi = np.array(d_all[1]), np.array(d_all[2])
    ax.plot(va[i[-n:]], vi[i[-n:]], 'kx')
    print('Lowest')
    for j in range(n):
        print(f'{1 + j}. {pubs[d_all[0][i[j]]]}')
    print()
    print('Highest')
    for j in range(n):
        print(f'{1 + j}. {pubs[d_all[0][i[-j - 1]]]}')

fname = 'f2-correlation.pdf'
print(f'Saving to {fname}')
fig.savefig(fname, dpi=300)
