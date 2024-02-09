#!/usr/bin/env python3
#
# Figure 3: Highlighted subgroups
#
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import base


# Gather data
print('Gathering data')
with base.connect() as con:
    c = con.cursor()

    q = ('select va, vi, sequence, beta1, cell from midpoints_wt'
         ' where (ni > 0 and na > 0)')
    p = [row for row in c.execute(q)]


#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(9, 3.82))    # Two column size
fig.subplots_adjust(0.08, 0.115, 0.98, 0.88, wspace=0.1)
xlim = -62, -19
ylim = -109, -59
# NOTE: These measurements picked to manually give axes equal aspect
grid = fig.add_gridspec(1, 3)

c1 = None # 'tab:green'
c2 = None # 'tab:purple'
c3 = None # 'tab:brown'
c4 = None # 'tab:brown'
c5 = '#aaa'
m1 = 'o'
m2 = 's'
m3 = '^'
m4 = '*'
m5 = 'v'

ax11 = fig.add_subplot(grid[0, 0])
ax11.set_xlabel('$\mu_a$ (mV)')
ax11.set_ylabel('$\mu_i$ (mV)')
ax11.grid(True, ls=':')
ax11.set_xlim(*xlim)
ax11.set_ylim(*ylim)

ax12 = fig.add_subplot(grid[0, 1])
ax12.set_xlabel('$\mu_a$ (mV)')
ax12.set_yticklabels([])
ax12.grid(True, ls=':')
ax12.set_xlim(*xlim)
ax12.set_ylim(*ylim)

ax13 = fig.add_subplot(grid[0, 2])
ax13.set_xlabel('$\mu_a$ (mV)')
ax13.set_yticklabels([])
ax13.grid(True, ls=':')
ax13.set_xlim(*xlim)
ax13.set_ylim(*ylim)

# Subunit
kwargs = dict(ls='none', lw=5, markersize=6, markerfacecolor='none',
              alpha=0.65, rasterized=True)
del(kwargs['markerfacecolor'])
leg = dict(frameon=False, handlelength=0.15)
sub = ['a', 'astar', 'b', 'bstar']
v = np.array([r[:2] for r in p if r[2] == 'astar'])
ax11.plot(v[:, 0], v[:, 1], m1, label=f'a* ({len(v)})', **kwargs)
v = np.array([r[:2] for r in p if r[2] == 'b'])
ax11.plot(v[:, 0], v[:, 1], m2, label=f'b ({len(v)})', **kwargs)
v = np.array([r[:2] for r in p if r[2] not in sub])
ax11.plot(v[:, 0], v[:, 1], m5, color='#ccc', label=f'? ({len(v)})', **kwargs)
v = np.array([r[:2] for r in p if r[2] == 'a'])
ax11.plot(v[:, 0], v[:, 1], m3, label=f'a ({len(v)})', **kwargs)
v = np.array([r[:2] for r in p if r[2] == 'bstar'])
ax11.plot(v[:, 0], v[:, 1], m4, label=f'b* ({len(v)})', **kwargs)
ax11.legend(ncol=3, loc=(0.05, 0.995), **leg)

# Beta 1
v = np.array([r[:2] for r in p if r[3] == 'no'])
ax12.plot(v[:, 0], v[:, 1], m1, label=f'Without $\\beta1$ ({len(v)})',
          **kwargs)
v = np.array([r[:2] for r in p if r[3] == 'yes'])
ax12.plot(v[:, 0], v[:, 1], m2, label=f'With $\\beta1$ ({len(v)})', **kwargs)
ax12.legend(ncol=1, loc=(0.10, 0.995), **leg)

# Cell type
v = np.array([r[:2] for r in p if r[4] == 'HEK'])
ax13.plot(v[:, 0], v[:, 1], m1, label=f'HEK ({len(v)})', **kwargs)
v = np.array([r[:2] for r in p if r[4] == 'CHO'])
ax13.plot(v[:, 0], v[:, 1], m2, label=f'CHO ({len(v)})', **kwargs)
v = np.array([r[:2] for r in p if r[4] == 'Oocyte'])
ax13.plot(v[:, 0], v[:, 1], m3, label=f'Oocyte ({len(v)})', **kwargs)
ax13.legend(ncol=2, loc=(0.10, 0.995), **leg)

y = 0.105
base.axletter(ax11, 'A', tweak=y, offset=-0.065)
base.axletter(ax12, 'B', tweak=y, offset=0.004)
base.axletter(ax13, 'C', tweak=y, offset=0.004)

fname = 'f3-subgroups' + ('.png' if 'png' in sys.argv else '.pdf')
print(f'Saving to {fname}')
fig.savefig(fname)
