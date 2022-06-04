#!/usr/bin/env python3
#
# Figure 1: Reconstructed histograms of midpoints of inactivation and
# activation.
#
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import base


# Get data
with base.connect() as con:

    # Get myocyte data
    c = con.cursor()
    q = 'select pub, va, sema, na, stda from midpoints_myo'
    da_myo = base.individual_pdfs(c.execute(q))
    q = 'select pub, vi, semi, ni, stdi from midpoints_myo'
    di_myo = base.individual_pdfs(c.execute(q))

    a = 'select pub, va, sema, na, stda from midpoints_wt'
    i = 'select pub, vi, semi, ni, stdi from midpoints_wt'
    da_wt = base.combined_pdf(c.execute(a))
    di_wt = base.combined_pdf(c.execute(i))

myo_options = {
    'Feng 1996': ['Feng atrium', 'k', ':', '|'],
    'Sakakibara 1992': ['Sakakibara atrium', 'tab:purple', '-.', '/'],
    'Sakakibara 1993': ['Sakakibara ventricle', 'tab:cyan', '-', '\\'],
    'Schneider 1994': ['Schneider atrium', 'tab:olive', '--', '-'],
}
for a, i in zip(da_myo, di_myo):
    if a[1] == i[1]:
        myo_options[a[0]][0] += f' (n={a[1]})'
    else:
        myo_options[a[0]][0] += f' (n={i[1]}, {a[1]})'

# Show reconstructed histogram data
print('Reconstructed Va distribution:')
print(f'  mean : {da_wt[3]}')
print(f'  sigma: {da_wt[4]}')
print('Reconstructed Vi distribution:')
print(f'  mean : {di_wt[3]}')
print(f'  sigma: {di_wt[4]}')


#
# Create figure
#
print('Creating figure')
fig = plt.figure(figsize=(6, 6))    # Two-third-column size
fig.subplots_adjust(0.06, 0.075, 0.99, 0.99, hspace=0.12)

xlim = -120, -10

ax = fig.add_subplot(2, 1, 1)
for s in ax.spines.values():
    s.set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
ax.get_yaxis().set_visible(False)
ax.set_xlim(*xlim)
ax.set_xticklabels([])
ax.set_ylim(0, 3.6)
offset, tweak = -0.04, 0
base.axletter(ax, 'A', offset=offset, tweak=tweak)

grey = '#bbbbbb'
for pub, n, x, y, mu, sigma in di_myo:
    label, color, ls, hatch = myo_options[pub]
    ax.plot((mu, mu), (0, np.max(y)), color=grey, zorder=0, lw=1)
    ax.plot(x, y, color=color, ls=ls, label=label)
for pub, n, x, y, mu, sigma in da_myo:
    label, color, ls, hatch = myo_options[pub]
    ax.plot((mu, mu), (0, np.max(y)), color=grey, zorder=0, lw=1)
    ax.plot(x, y, color=color, ls=ls)
    #ax.fill_between(x, y, fc='none', ec=color, hatch=hatch, zorder=0)
ax.legend(loc=(0, 0.85), frameon=False, ncol=2)


ax = fig.add_subplot(2, 1, 2)
for s in ax.spines.values():
    s.set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
ax.get_yaxis().set_visible(False)
ax.set_xlim(*xlim)
ax.set_xlabel('Membrane potential (mV)')
ax.set_ylim(0, 0.054)
base.axletter(ax, 'B', offset=offset, tweak=tweak)

xa, ya, za = da_wt[0]
xi, yi, zi = di_wt[0]
labela = f'Activation (m={da_wt[1]}, n={da_wt[2]})'
labeli = f'Inactivation (m={di_wt[1]}, n={di_wt[2]})'
ca = 'tab:blue'
ci = 'tab:orange'
ma, mi = da_wt[3], di_wt[3]

ax.fill_between(xa, ya, ec=ca, fc='none', hatch='///')
ax.fill_between(xi, yi, ec=ci, fc='none', hatch='\\\\\\')
ax.plot(xa, ya, color=ca, label=labela)
ax.plot(xi, yi, color=ci, label=labeli)
ax.plot((ma, ma), (0, np.max(za)), color=grey)
ax.plot((mi, mi), (0, np.max(zi)), color=grey)
ax.plot(xa, za, color=ca, ls='--', lw=3)
ax.plot(xi, zi, color=ci, ls='--', lw=3)

ax.legend(loc=(0, 0.85), frameon=False)

# Save
fname = 'f1-combined.pdf'
print(f'Saving to {fname}')
fig.savefig(fname)
