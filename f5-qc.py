#!/usr/bin/env python3
#
# Figure 5: Highlighted subgroups
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
fig = plt.figure(figsize=(9, 7.9))        # Two column size
fig.subplots_adjust(0.08, 0.06, 0.985, 0.940, wspace=0.3, hspace=0.36)

xlim = -62, -19
ylim = -109, -59
# NOTE: These measurements picked to manually give axes equal aspect
grid = fig.add_gridspec(2, 3)

c1 = None  # 'tab:green'
c2 = None  # 'tab:purple'
c3 = None  # 'tab:brown'
c4 = None  # 'tab:brown'
c5 = '#aaa'
m1 = 'o'
m2 = 's'
m3 = '^'
m4 = '*'
m5 = 'v'

'''
ax11 = fig.add_subplot(grid[0, 0])
ax11.set_xlabel(r'$\mu_a$ (mV)')
ax11.set_ylabel(r'$\mu_i$ (mV)')
ax11.grid(True, ls=':')
ax11.set_xlim(*xlim)
ax11.set_ylim(*ylim)

ax12 = fig.add_subplot(grid[0, 1])
ax12.set_xlabel(r'$\mu_a$ (mV)')
ax12.set_yticklabels([])
ax12.grid(True, ls=':')
ax12.set_xlim(*xlim)
ax12.set_ylim(*ylim)

ax13 = fig.add_subplot(grid[0, 2])
ax13.set_xlabel(r'$\mu_a$ (mV)')
ax13.set_yticklabels([])
ax13.grid(True, ls=':')
ax13.set_xlim(*xlim)
ax13.set_ylim(*ylim)

ax21 = fig.add_subplot(grid[1, 0])
ax21.set_xlabel(r'$\mu_a$ (mV)')
ax21.set_ylabel(r'$\mu_i$ (mV)')
ax21.grid(True, ls=':')
ax21.set_xlim(*xlim)
ax21.set_ylim(*ylim)

ax22 = fig.add_subplot(grid[1, 1])
ax22.set_xlabel(r'$\mu_a$ (mV)')
ax22.set_yticklabels([])
ax22.grid(True, ls=':')
ax22.set_xlim(*xlim)
ax22.set_ylim(*ylim)

ax23 = fig.add_subplot(grid[1, 2])
ax23.set_xlabel(r'$\mu_a$ (mV)')
ax23.set_yticklabels([])
ax23.grid(True, ls=':')
ax23.set_xlim(*xlim)
ax23.set_ylim(*ylim)
'''


print('Gathering data')
with base.connect() as con:
    c = con.cursor()

    #q = ('select va, vi, sequence, beta1, cell, pub from midpoints_wt'
    #     f' where (ni > 0 and na > 0 {qand})')
    #p = [row for row in c.execute(q)]

    q = ('select irep, va from midpoints_wt'
         f' where (na > 0 and irep is not null and irep < 0 {qand})')
    p = np.array([row for row in c.execute(q)])
    x, y = -p[:, 0], p[:, 1]

    ax11 = fig.add_subplot(grid[0, 0])
    ax11.set_xlabel(r'Peak "representative" current (mV)')
    ax11.set_ylabel(r'$\mu_a$ (mV)')
    ax11.grid(True, ls=':')
    #ax11.set_xlim(*xlim)
    #ax11.set_ylim(*ylim)
    ax11.plot(x, y, 'o', markerfacecolor='none')

    # Fit line
    p = np.corrcoef(x, y)[1, 0]
    b, a = np.polyfit(x, y, 1)
    print('Fit to all data')
    print(f'  a, b: {a:.1f}, {b:.2f}')
    print(f'  Pearson correlation coefficient: {p:.2f}')
    print(f'                          squared: {p**2:.2f}')
    xx = np.linspace(np.min(x) - 500, np.max(x) + 500)
    ax11.plot(xx, a + b * xx)



    q = ('select irep, ka from midpoints_wt'
         f' where (ka is not null and irep is not null and irep < 0 {qand})')
    p = np.array([row for row in c.execute(q)])
    x, y = -p[:, 0], p[:, 1]

    ax12 = fig.add_subplot(grid[0, 1])
    ax12.set_xlabel(r'Peak "representative" current (mV)')
    ax12.set_ylabel(r'$k_a$')
    ax12.grid(True, ls=':')
    #ax11.set_xlim(*xlim)
    #ax11.set_ylim(*ylim)
    ax12.plot(x, y, 'o', markerfacecolor='none')

    # Fit line
    p = np.corrcoef(x, y)[1, 0]
    b, a = np.polyfit(x, y, 1)
    print('Fit to all data')
    print(f'  a, b: {a:.1f}, {b:.2f}')
    print(f'  Pearson correlation coefficient: {p:.2f}')
    print(f'                          squared: {p**2:.2f}')
    xx = np.linspace(np.min(x) - 500, np.max(x) + 500)
    ax12.plot(xx, a + b * xx)



    q = ('select ka, va from midpoints_wt'
         f' where (na > 0 and ka is not null {qand})')
    p = np.array([row for row in c.execute(q)])
    x, y = p[:, 0], p[:, 1]

    ax13 = fig.add_subplot(grid[0, 2])
    ax13.set_xlabel(r'$k_a$')
    ax13.set_ylabel(r'$\mu_a$ (mV)')
    ax13.grid(True, ls=':')
    #ax11.set_xlim(*xlim)
    #ax11.set_ylim(*ylim)
    ax13.plot(x, y, 'o', markerfacecolor='none')

    # Fit line
    p = np.corrcoef(x, y)[1, 0]
    b, a = np.polyfit(x, y, 1)
    print('Fit to all data')
    print(f'  a, b: {a:.1f}, {b:.2f}')
    print(f'  Pearson correlation coefficient: {p:.2f}')
    print(f'                          squared: {p**2:.2f}')
    xx = np.linspace(np.min(x) - 1, np.max(x) + 1)
    ax13.plot(xx, a + b * xx)




    q = ('select irep, vi from midpoints_wt'
         f' where (ni > 0 and irep is not null and irep < 0 {qand})')
    p = np.array([row for row in c.execute(q)])
    x, y = -p[:, 0], p[:, 1]

    ax21 = fig.add_subplot(grid[1, 0])
    ax21.set_xlabel(r'Peak "representative" current (mV)')
    ax21.set_ylabel(r'$\mu_i$ (mV)')
    ax21.grid(True, ls=':')
    #ax11.set_xlim(*xlim)
    #ax11.set_ylim(*ylim)
    ax21.plot(x, y, 'o', markerfacecolor='none')

    # Fit line
    p = np.corrcoef(x, y)[1, 0]
    b, a = np.polyfit(x, y, 1)
    print('Fit to all data')
    print(f'  a, b: {a:.1f}, {b:.2f}')
    print(f'  Pearson correlation coefficient: {p:.2f}')
    print(f'                          squared: {p**2:.2f}')
    xx = np.linspace(np.min(x) - 500, np.max(x) + 500)
    ax21.plot(xx, a + b * xx)



    q = ('select irep, ki from midpoints_wt'
         f' where (ki is not null and irep is not null and irep < 0 {qand})')
    p = np.array([row for row in c.execute(q)])
    x, y = -p[:, 0], p[:, 1]

    ax22 = fig.add_subplot(grid[1, 1])
    ax22.set_xlabel(r'Peak "representative" current (mV)')
    ax22.set_ylabel(r'$k_i$')
    ax22.grid(True, ls=':')
    #ax11.set_xlim(*xlim)
    #ax11.set_ylim(*ylim)
    ax22.plot(x, y, 'o', markerfacecolor='none')

    # Fit line
    p = np.corrcoef(x, y)[1, 0]
    b, a = np.polyfit(x, y, 1)
    print('Fit to all data')
    print(f'  a, b: {a:.1f}, {b:.2f}')
    print(f'  Pearson correlation coefficient: {p:.2f}')
    print(f'                          squared: {p**2:.2f}')
    xx = np.linspace(np.min(x) - 500, np.max(x) + 500)
    ax22.plot(xx, a + b * xx)



    q = ('select ki, vi from midpoints_wt'
         f' where (ni > 0 and ki is not null {qand})')
    p = np.array([row for row in c.execute(q)])
    x, y = p[:, 0], p[:, 1]

    ax23 = fig.add_subplot(grid[1, 2])
    ax23.set_xlabel(r'$k_i$')
    ax23.set_ylabel(r'$\mu_i$ (mV)')
    ax23.grid(True, ls=':')
    #ax11.set_xlim(*xlim)
    #ax11.set_ylim(*ylim)
    ax23.plot(x, y, 'o', markerfacecolor='none')

    # Fit line
    p = np.corrcoef(x, y)[1, 0]
    b, a = np.polyfit(x, y, 1)
    print('Fit to all data')
    print(f'  a, b: {a:.1f}, {b:.2f}')
    print(f'  Pearson correlation coefficient: {p:.2f}')
    print(f'                          squared: {p**2:.2f}')
    xx = np.linspace(np.min(x) - 1, np.max(x) + 1)
    ax23.plot(xx, a + b * xx)


'''
# Subunit
kwargs = dict(ls='none', lw=5, markersize=6, alpha=0.65, rasterized=True)
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
if len(v):
    ax13.plot(v[:, 0], v[:, 1], m3, label=f'Oocyte ({len(v)})', **kwargs)
ax13.legend(ncol=2, loc=(0.10, 0.995), **leg)

# Biggest subgroup
del kwargs['alpha'], kwargs['rasterized']
v = np.array(
    [r[:2] for r in p if r[2] == 'astar' and r[3] == 'yes' and r[4] == 'HEK'])
ax21.plot(v[:, 0], v[:, 1], '*', zorder=2, color='k',
          label=f'a*, with $\\beta1$, HEK ({len(v)})', **kwargs)
v = np.array(
    [r[:2] for r in p if r[2] != 'astar' or r[3] != 'yes' or r[4] != 'HEK'])
ax21.plot(v[:, 0], v[:, 1], 'o', zorder=1, color='#ccc',
          label=f'Other ({len(v)})', **kwargs)
ax21.legend(ncol=1, loc=(0.10, 0.995), **leg)

# Linear fit
v = np.array([r[:2] for r in p])
b1, a1 = np.polyfit(v[:, 0], v[:, 1], 1)
x = np.array(xlim)
y = a1 + b1 * x

# Kapplinger
ax22.plot(x, y, '-', color='tab:blue', zorder=4)
v = np.array([r[:2] for r in p if r[5] == 'Kapplinger 2015'])
ax22.plot(v[:, 0], v[:, 1], '*', zorder=3, color='k',
          label=f'Kapplinger et al. 2015 ({len(v)})', **kwargs)
v = np.array([r[:2] for r in p if r[5] != 'Kapplinger 2015'])
ax22.plot(v[:, 0], v[:, 1], 'o', zorder=2, color='#ccc',
          label=f'Other ({len(v)})', **kwargs)
ax22.legend(ncol=1, loc=(0.10, 0.995), **leg)

# Tan
ax23.plot(x, y, '-', color='tab:blue', zorder=4)
v = np.array([r[:2] for r in p if r[5] == 'Tan 2005'])
ax23.plot(v[:, 0], v[:, 1], '*', zorder=3, color='k',
          label=f'Tan et al. 2005 ({len(v)})', **kwargs)
v = np.array([r[:2] for r in p if r[5] != 'Tan 2005'])
ax23.plot(v[:, 0], v[:, 1], 'o', zorder=2, color='#ccc',
          label=f'Other ({len(v)})', **kwargs)
ax23.legend(ncol=1, loc=(0.10, 0.995), **leg)
'''

#y = 0.105
x0 = -0.069
x1 = 0
y0 = 0.055
y1 = 0.052
#base.axletter(ax11, 'A', tweak=y0, offset=x0)
#base.axletter(ax12, 'B', tweak=y0, offset=x1)
#base.axletter(ax13, 'C', tweak=y0, offset=x1)
#base.axletter(ax21, 'D', tweak=y1, offset=x0)
#base.axletter(ax22, 'E', tweak=y1, offset=x1)
#base.axletter(ax23, 'F', tweak=y1, offset=x1)

fname = 'f5-qc' + ('.png' if 'png' in sys.argv else '.pdf')
print(f'Saving to {fname}')
fig.savefig(fname)
