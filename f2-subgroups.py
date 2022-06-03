#!/usr/bin/env python3
#
# Figure 2: Reconstructed histograms for subgroups.
#
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import base


# Get data
print('Fetching data...')
with base.connect() as con:

    # All data
    c = con.cursor()
    a = 'select pub, va, sema, na, stda from midpoints_wt'
    i = 'select pub, vi, semi, ni, stdi from midpoints_wt'
    da_wt = base.combined_pdf(c.execute(a))
    di_wt = base.combined_pdf(c.execute(i))

    # Biggest subgroup
    r = ' where sequence == "astar" and cell == "HEK" and beta1 == "yes"'
    da_big = base.combined_pdf(c.execute(a + r))
    di_big = base.combined_pdf(c.execute(i + r))

    if 'debug' in sys.argv:
        da_a = da_b = da_as = da_bs = da_wt
        da_b1 = da_nob1 = da_hek = da_cho = da_ooc = da_wt
        di_a = di_b = di_as = di_bs = di_wt
        di_b1 = di_nob1 = di_hek = di_cho = di_ooc = di_wt
    else:
        # Isoforms
        r = ' where sequence == "a"'
        da_a = base.combined_pdf(c.execute(a + r))
        di_a = base.combined_pdf(c.execute(i + r))
        r = ' where sequence == "b"'
        da_b = base.combined_pdf(c.execute(a + r))
        di_b = base.combined_pdf(c.execute(i + r))
        r = ' where sequence == "astar"'
        da_as = base.combined_pdf(c.execute(a + r))
        di_as = base.combined_pdf(c.execute(i + r))
        r = ' where sequence == "bstar"'
        da_bs = base.combined_pdf(c.execute(a + r))
        di_bs = base.combined_pdf(c.execute(i + r))
        #r = ' where sequence is null'
        #da_u = base.combined_pdf(c.execute(a + r))
        #di_u = base.combined_pdf(c.execute(i + r))

        # With beta1
        r = ' where beta1 == "yes"'
        da_b1 = base.combined_pdf(c.execute(a + r))
        di_b1 = base.combined_pdf(c.execute(i + r))
        r = ' where beta1 == "no"'
        da_nob1 = base.combined_pdf(c.execute(a + r))
        di_nob1 = base.combined_pdf(c.execute(i + r))

        # Cell types
        r = ' where cell == "HEK"'
        da_hek = base.combined_pdf(c.execute(a + r))
        di_hek = base.combined_pdf(c.execute(i + r))
        r = ' where cell == "CHO"'
        da_cho = base.combined_pdf(c.execute(a + r))
        di_cho = base.combined_pdf(c.execute(i + r))
        r = ' where cell == "Oocyte"'
        da_ooc = base.combined_pdf(c.execute(a + r))
        di_ooc = base.combined_pdf(c.execute(i + r))


#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(9, 8))    # Two-column size
fig.subplots_adjust(0.03, 0.065, 0.995, 1, hspace=0.5, wspace=0.2)
grid = fig.add_gridspec(5, 3)

xlim = -120, -10


def sub(ax, a, i, top=False, xlabel=False, name=None, ylim=None):
    for s in ax.spines.values():
        s.set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(20))
    ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
    ax.get_yaxis().set_visible(False)
    ax.set_xlim(*xlim)

    if xlabel:
        ax.set_xlabel('Membrane potential (mV)')
    else:
        ax.set_xticklabels([])

    if top:
        ca, ci = 'tab:blue', 'tab:orange'
    else:
        ca, ci = 'tab:pink', 'tab:brown'

    la = li = None
    if name:
        la = f'$V_a$, {name} (m={a[1]}, n={a[2]})'
        li = f'$V_i$, {name} (m={i[1]}, n={i[2]})'

    xa, ya, za = a[0]
    xi, yi, zi = i[0]

    grey = '#555555'
    ax.fill_between(xa, ya, ec=ca, fc='none', hatch=4 * '/')
    ax.fill_between(xi, yi, ec=ci, fc='none', hatch=4 * '\\')
    ax.plot(xa, ya, color=ca, label=la)
    ax.plot(xi, yi, color=ci, label=li)
    ax.plot((a[3], a[3]), (0, np.max(za)), color=grey)
    ax.plot((i[3], i[3]), (0, np.max(zi)), color=grey)
    ax.plot(xa, za, color=ca, ls='--', lw=2)
    ax.plot(xi, zi, color=ci, ls='--', lw=2)
    ax.grid(True, color='#cccccc', ls=':')

    if name:
        ax.legend(loc=(0, 0.95), frameon=False, fontsize=9)

    if ylim is None:
        ylim = max(np.max(ya), np.max(za),
                   np.max(yi), np.max(zi)) * 1.03
    ax.set_ylim(0, ylim)


ax00 = fig.add_subplot(grid[0, 0])
ax01 = fig.add_subplot(grid[0, 1])
ax02 = fig.add_subplot(grid[0, 2])
sub(ax00, da_wt, di_wt, top=True)
sub(ax01, da_wt, di_wt, top=True)
sub(ax02, da_wt, di_wt, top=True)

ax10 = fig.add_subplot(grid[1, 0])
ax20 = fig.add_subplot(grid[2, 0])
ax30 = fig.add_subplot(grid[3, 0])
ax40 = fig.add_subplot(grid[4, 0])
sub(ax10, da_a, di_a, name='a')
sub(ax20, da_b, di_b, name='b')
sub(ax30, da_as, di_as, name='a*')
sub(ax40, da_bs, di_bs, name='b*', ylim=0.05, xlabel=True)

ax11 = fig.add_subplot(grid[1, 1])
ax21 = fig.add_subplot(grid[2, 1])
sub(ax11, da_b1, di_b1, name=r'With ${\beta}1$')
sub(ax21, da_nob1, di_nob1, name=r'Without ${\beta}1$', xlabel=True)

ax12 = fig.add_subplot(grid[1, 2])
ax22 = fig.add_subplot(grid[2, 2])
ax32 = fig.add_subplot(grid[3, 2])
sub(ax12, da_hek, di_hek, name='HEK')
sub(ax22, da_cho, di_cho, name='CHO')
sub(ax32, da_ooc, di_ooc, name='Oocytes', xlabel=True)

ax41 = fig.add_subplot(grid[4, 1])
sub(ax41, da_big, di_big, name=r'a*, ${\beta}1$, HEK', xlabel=True, top=True)

of, tw = -0.018, -0.005
base.axletter(ax00, 'A', offset=of, tweak=tw)
base.axletter(ax01, 'B', offset=of, tweak=tw)
base.axletter(ax02, 'C', offset=of, tweak=tw)
base.axletter(ax41, 'D', offset=of, tweak=0.041)


fname = 'f2-subgroups.pdf'
print(f'Saving to {fname}')
fig.savefig(fname)
