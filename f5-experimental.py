#!/usr/bin/env python3
#
# Figure 4: Highlighted subgroups
#
import sys

import numpy as np
import matplotlib.pyplot as plt

import base

# Exclude ooocytes
nooocytes = True
qand = 'and cell != "Oocyte"' if nooocytes else ''


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


# Gather data
print('Gathering data')
with base.connect() as con:
    c = con.cursor()

    q = ('select va, vi, sequence, beta1, cell, ljp_corrected, pub'
         f' from midpoints_wt where (ni > 0 and na > 0 {qand})')
    p = [row for row in c.execute(q)]

    # Activation slope
    x_vaka, y_vaka = va('ka')
    # V peak
    x_vpeak, y_vpeak = va('vpeak')
    # Holding potential
    x_vapah, y_vapah = va('pah')
    x_vipih, y_vipih = vi('pih')


#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(9, 4.2))        # Two column size
fig.subplots_adjust(bottom=0.11)
gr1 = fig.add_gridspec(1, 1, left=0.08, right=0.45, top=0.85)
gr2 = fig.add_gridspec(2, 2, left=0.56, right=0.97, top=0.92,
                       wspace=0.6, hspace=0.6)

# LJP Correction
xlim = -62, -19
ylim = -109, -59
c5 = '#aaa'
m1 = 'o'
m2 = 's'
m3 = '^'

ax11 = fig.add_subplot(gr1[0, 0])
ax11.set_xlabel(r'$\mu_a$ (mV)')
ax11.set_ylabel(r'$\mu_i$ (mV)')
ax11.grid(True, ls=':')
ax11.set_xlim(*xlim)
ax11.set_ylim(*ylim)

kwargs = dict(ls='none', lw=5, markersize=6, alpha=0.65, rasterized=True)
leg = dict(frameon=False, handlelength=0.15)

v = np.array([r[:2] for r in p if r[5] == 'yes'])
ax11.plot(v[:, 0], v[:, 1], m3, label=f'Corrected LJP ({len(v)})', **kwargs)
v = np.array([r[:2] for r in p if r[5] == 'no'])
ax11.plot(v[:, 0], v[:, 1], m2, label=f'Did not correct LJP ({len(v)})',
          **kwargs)
v = np.array([r[:2] for r in p if r[5] is None])
ax11.plot(v[:, 0], v[:, 1], m1, label=f'Not reported ({len(v)})',
          color=c5, zorder=1, **kwargs)
ax11.legend(loc=(0.04, 0.995), **leg)

#
# Holding potential
#
ax12 = fig.add_subplot(gr2[0, 0])
ax12.set_xlabel(r'$V_{hold,a}$')
ax12.set_ylabel(r'$\mu_a$ (mV)')
ax12.grid(True, ls=':')
ax12.plot(x_vapah, y_vapah, 'o', markerfacecolor='none')
fit_line(ax12, x_vapah, y_vapah)

ax13 = fig.add_subplot(gr2[0, 1])
ax13.set_xlabel(r'$V_{hold,i}$')
ax13.set_ylabel(r'$\mu_i$ (mV)')
ax13.grid(True, ls=':')
ax13.plot(x_vipih, y_vipih, 'o', markerfacecolor='none')
fit_line(ax13, x_vipih, y_vipih)

#
# Voltage control
#
ax22 = fig.add_subplot(gr2[1, 0])
ax22.set_xlabel('$k_a$')
ax22.text(-0.2, -0.29, 'More steep', transform=ax22.transAxes)
ax22.text(1.18, -0.29, 'Less steep', ha='right', transform=ax22.transAxes)
ax22.set_ylabel(r'$\mu_a$ (mV)')
ax22.grid(True, ls=':')
ax22.plot(x_vaka, y_vaka, 'o', markerfacecolor='none')
fit_line(ax22, x_vaka, y_vaka)

#
# Voltage-shift
#
ax23 = fig.add_subplot(gr2[1, 1])
ax23.set_xlabel(r'$V_{peak}$ (mV)')
ax23.set_ylabel(r'$\mu_a$ (mV)')
ax23.grid(True, ls=':')
ax23.plot(x_vpeak, y_vpeak, 'o', markerfacecolor='none')
fit_line(ax23, x_vpeak, y_vpeak)



#
# Finish and save
#
x, y = -0.06, 0.07
base.axletter(ax11, 'A', tweak=0.14, offset=-0.069)
base.axletter(ax12, 'B', tweak=y, offset=x)
base.axletter(ax13, 'C', tweak=y, offset=x)
base.axletter(ax22, 'D', tweak=y, offset=x)
base.axletter(ax23, 'E', tweak=y, offset=x)

fname = 'f5-experimental' + ('.png' if 'png' in sys.argv else '.pdf')
print(f'Saving to {fname}')
fig.savefig(fname)
