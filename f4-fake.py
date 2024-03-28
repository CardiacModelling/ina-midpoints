#!/usr/bin/env python3
#
# Figure 3: Highlighted subgroups
#
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import base

nooocytes = True


# Gather data
print('Gathering data')
with base.connect() as con:
    c = con.cursor()

    qand = ' and cell != "Oocyte"' if nooocytes else ''
    q = f'select va, vi from midpoints_wt where (ni > 0 and na > 0) {qand}'
    p = [row for row in c.execute(q)]
    va = np.array([r[0] for r in p])
    vi = np.array([r[1] for r in p])
    n = len(va)
    

#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(9, 2.7))    # Two column size
fig.subplots_adjust(0.08, 0.115, 0.98, 0.88, wspace=0.1)
grid = fig.add_gridspec(1, 4)
xlim = -67, -14
ylim = -114, -54
# NOTE: These measurements picked to manually give axes equal aspect

kwargs = dict(ls='none', lw=5, markersize=6,
              markeredgecolor='k', markerfacecolor='none')
#leg = dict(frameon=False, handlelength=0.15)

ax0 = fig.add_subplot(grid[0, 0])
ax0.set_xlabel(r'$\mu_a$ (mV)')
ax0.set_ylabel(r'$\mu_i$ (mV)')
ax0.grid(True, ls=':')
ax0.set_xlim(*xlim)
ax0.set_ylim(*ylim)
ax0.plot(va, vi, 'o', **kwargs)
#ax0.legend(ncol=1, loc=(0.10, 0.995), **leg)

fax = []
for i in range(3):
    ax = fig.add_subplot(grid[0, 1 + i])
    ax.set_xlabel(r'$\mu_a$ (mV)')
    ax.set_yticklabels([])
    ax.grid(True, ls=':')
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    fax.append(ax)


# Synthetic data
for ax in fax:
    if False:
        vcor = 15
        vind = 7
        mu = np.random.uniform(-40 - vcor, -40 + vcor, size=n)
        mua = mu + np.random.uniform(-vind, vind, size=n)
        mui = mu - 43.43 + np.random.uniform(-vind, vind, size=n)
        ax.plot(mua, mui, 'o', **kwargs)
    else:
        scor = 7
        sind = 4
        mu = np.random.normal(-40, scor, size=n)
        mua = np.random.normal(mu, sind, size=n)
        mui = np.random.normal(mu - 43.43, sind, size=n)
        ax.plot(mua, mui, 'o', **kwargs)


#y = 0.06
#base.axletter(ax0, 'A', tweak=y, offset=-0.1)
#base.axletter(fax[0], 'B', tweak=y, offset=0)

fname = 'f4-synthetic' + ('.png' if 'png' in sys.argv else '.pdf')
print(f'Saving to {fname}')
fig.savefig(fname)
