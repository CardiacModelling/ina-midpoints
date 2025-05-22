#!/usr/bin/env python3
#
# Figure 5: Linear correlations
#
import sys

import numpy as np
import matplotlib.pyplot as plt

import base

# Exclude ooocytes
nooocytes = True
qand = 'and cell != "Oocyte"' if nooocytes else ''

#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(9, 10))        # Two column size
fig.subplots_adjust(0.08, 0.055, 0.99, 0.97, wspace=0.5, hspace=0.55)
grid = fig.add_gridspec(5, 4)


def fit_line(ax, x, y):
    """ Fit line to x and y and plot on ax """
    p = np.corrcoef(x, y)[1, 0]
    b, a = np.polyfit(x, y, 1)

    lo, hi = np.min(x), np.max(x)
    pad = 0.05 * (hi - lo)
    xx = np.linspace(lo - pad, hi + pad)
    ax.plot(xx, a + b * xx)
    ax.text(1, 1.01, f'$n={len(x)}$, $r^2={p**2:.2f}$',
            ha='right', va='bottom', transform=ax.transAxes)


def va(factor, extra=''):
    """ Fetch data for Va and given factor """
    q = (f'select {factor}, va from midpoints_wt'
         f' where (na > 0 and {factor} is not null {extra} {qand})')
    p = np.array([row for row in c.execute(q)])
    return p[:, 0], p[:, 1]


def vi(factor):
    """ Fetch data for Vi and given factor """
    q = (f'select {factor}, vi from midpoints_wt'
         f' where (ni > 0 and {factor} is not null {qand})')
    p = np.array([row for row in c.execute(q)])
    return p[:, 0], p[:, 1]


def stda(factor, extra=''):
    """ Fetch data for Sigma-a and given factor """
    q = (f'select {factor}, stda from midpoints_wt'
         f' where (na > 0 and {factor} is not null {extra} {qand})')
    p = np.array([row for row in c.execute(q)])
    return p[:, 0], p[:, 1]


def stdi(factor):
    """ Fetch data for Sigma-i and given factor """
    q = (f'select {factor}, stdi from midpoints_wt'
         f' where (ni > 0 and {factor} is not null {qand})')
    p = np.array([row for row in c.execute(q)])
    return p[:, 0], p[:, 1]



print('Gathering data')
with base.connect() as con:
    c = con.cursor()

    #
    # Ka on Va
    #
    ax00 = fig.add_subplot(grid[0, 0])
    ax00.set_xlabel('$k_a$')
    ax00.text(-0.2, -0.25, 'More steep', transform=ax00.transAxes)
    ax00.text(1.2, -0.25, 'Less steep', ha='right', transform=ax00.transAxes)
    ax00.set_ylabel(r'$\mu_a$ (mV)')
    ax00.grid(True, ls=':')
    x, y = va('ka')
    ax00.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax00, x, y)

    #
    # I-representative on Va
    #
    ax01 = fig.add_subplot(grid[0, 1])
    ax01.set_xlabel('Peak representative I (nA)')
    ax01.set_ylabel(r'$\mu_a$ (mV)')
    ax01.grid(True, ls=':')
    x, y = va('irep', 'and irep < 0')
    x *= 1e-3
    ax01.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax01, x, y)

    #
    # Vhold,a and Vhold,i on Va and Vi
    #
    x, y = va('pah')
    ax02 = fig.add_subplot(grid[0, 2])
    ax02.set_xlabel(r'$V_{hold,a}$ (mV)')
    ax02.set_ylabel(r'$\mu_a$ (mV)')
    ax02.grid(True, ls=':')
    ax02.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax02, x, y)

    x, y = vi('pih')
    ax03 = fig.add_subplot(grid[0, 3])
    ax03.set_xlabel(r'$V_{hold,i}$ (mV)')
    ax03.set_ylabel(r'$\mu_i$ (mV)')
    ax03.grid(True, ls=':')
    ax03.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax03, x, y)

    #
    # [Na]e on Va and Vi
    #
    ax10 = fig.add_subplot(grid[1, 0])
    ax10.set_xlabel('$[Na^+]_e$ (mM)')
    ax10.set_ylabel(r'$\mu_a$ (mV)')
    ax10.grid(True, ls=':')
    x, y = va('na_e')
    ax10.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax10, x, y)

    ax11 = fig.add_subplot(grid[1, 1])
    ax11.set_xlabel('$[Na^+]_e$ (mM)')
    ax11.set_ylabel(r'$\mu_i$ (mV)')
    ax11.grid(True, ls=':')
    x, y = vi('na_e')
    ax11.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax11, x, y)

    #
    # [Na]i on Va and Vi
    #
    ax12 = fig.add_subplot(grid[1, 2])
    ax12.set_xlabel('$[Na^+]_i$ (mM)')
    ax12.set_ylabel(r'$\mu_a$ (mV)')
    ax12.grid(True, ls=':')
    x, y = va('na_i')
    ax12.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax12, x, y)

    ax13 = fig.add_subplot(grid[1, 3])
    ax13.set_xlabel('$[Na^+]_i$ (mM)')
    ax13.set_ylabel(r'$\mu_i$ (mV)')
    ax13.grid(True, ls=':')
    x, y = vi('na_i')
    ax13.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax13, x, y)

    #
    # [Ca]e on Va and Vi
    #
    ax20 = fig.add_subplot(grid[2, 0])
    ax20.set_xlabel('$[Ca^{2+}]_e$ (mM)')
    ax20.set_ylabel(r'$\mu_a$ (mV)')
    ax20.grid(True, ls=':')
    x, y = va('ca_e')
    ax20.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax20, x, y)

    ax21 = fig.add_subplot(grid[2, 1])
    ax21.set_xlabel('$[Ca^{2+}]_e$ (mM)')
    ax21.set_ylabel(r'$\mu_i$ (mV)')
    ax21.grid(True, ls=':')
    x, y = vi('ca_e')
    ax21.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax21, x, y)

    #
    # [Ca]i on Va and Vi
    #
    ax22 = fig.add_subplot(grid[2, 2])
    ax22.set_xlabel('$[Ca^{2+}]_{i,b}$ ($\mu$M)')
    ax22.set_ylabel(r'$\mu_a$ (mV)')
    ax22.grid(True, ls=':')
    x, y = va('ca_ib')
    x*= 1e3
    ax22.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax22, x, y)

    ax23 = fig.add_subplot(grid[2, 3])
    ax23.set_xlabel('$[Ca^{2+}]_{i,b}$ ($\mu$M)')
    ax23.set_ylabel(r'$\mu_i$ (mV)')
    ax23.grid(True, ls=':')
    x, y = vi('ca_ib')
    x*= 1e3
    ax23.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax23, x, y)

    #
    # [Cl]e on Va and Vi
    #
    ax30 = fig.add_subplot(grid[3, 0])
    ax30.set_xlabel('$[Cl^{-}]_e$')
    ax30.set_ylabel(r'$\mu_a$ (mV)')
    ax30.grid(True, ls=':')
    x, y = va('cl_e')
    ax30.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax30, x, y)

    ax31 = fig.add_subplot(grid[3, 1])
    ax31.set_xlabel('$[Cl^{-}]_e$')
    ax31.set_ylabel(r'$\mu_i$ (mV)')
    ax31.grid(True, ls=':')
    x, y = vi('cl_e')
    ax31.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax31, x, y)

    #
    # [Cl]i on Va and Vi
    #
    ax32 = fig.add_subplot(grid[3, 2])
    ax32.set_xlabel('$[Cl^{-}]_i$')
    ax32.set_ylabel(r'$\mu_a$ (mV)')
    ax32.grid(True, ls=':')
    x, y = va('cl_i')
    ax32.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax32, x, y)

    ax33 = fig.add_subplot(grid[3, 3])
    ax33.set_xlabel('$[Cl^{-}]_i$')
    ax33.set_ylabel(r'$\mu_i$ (mV)')
    ax33.grid(True, ls=':')
    x, y = vi('cl_i')
    ax33.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax33, x, y)

    #
    # [Cl]e on Sigma-a and Sigma-i
    #
    ax40 = fig.add_subplot(grid[4, 0])
    ax40.set_xlabel('$[Cl^{-}]_e$')
    ax40.set_ylabel(r'$\sigma_a$ (mV)')
    ax40.grid(True, ls=':')
    x, y = stda('cl_e')
    ax40.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax40, x, y)

    ax41 = fig.add_subplot(grid[4, 1])
    ax41.set_xlabel('$[Cl^{-}]_e$')
    ax41.set_ylabel(r'$\sigma_i$ (mV)')
    ax41.grid(True, ls=':')
    x, y = stdi('cl_e')
    ax41.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax41, x, y)

    #
    # [Cl]i Sigma-a and Sigma-i
    #
    ax42 = fig.add_subplot(grid[4, 2])
    ax42.set_xlabel('$[Cl^{-}]_i$')
    ax42.set_ylabel(r'$\sigma_a$ (mV)')
    ax42.grid(True, ls=':')
    x, y = stda('cl_i')
    ax42.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax42, x, y)

    ax43 = fig.add_subplot(grid[4, 3])
    ax43.set_xlabel('$[Cl^{-}]_i$')
    ax43.set_ylabel(r'$\sigma_i$ (mV)')
    ax43.grid(True, ls=':')
    x, y = stdi('cl_i')
    ax43.plot(x, y, 'o', markerfacecolor='none')
    fit_line(ax43, x, y)

#y = 0.105
#x0 = -0.069
#x1 = 0
#y0 = 0.055
#y1 = 0.052
#base.axletter(ax11, 'A', tweak=y0, offset=x0)
#base.axletter(ax12, 'B', tweak=y0, offset=x1)
#base.axletter(ax13, 'C', tweak=y0, offset=x1)
#base.axletter(ax21, 'D', tweak=y1, offset=x0)
#base.axletter(ax22, 'E', tweak=y1, offset=x1)
#base.axletter(ax23, 'F', tweak=y1, offset=x1)

fname = 's1-regression' + ('.png' if 'png' in sys.argv else '.pdf')
print(f'Saving to {fname}')
fig.savefig(fname)
