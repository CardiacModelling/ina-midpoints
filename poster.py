#!/usr/bin/env python3
#
# Poster figure
#
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy

import base

# Sigma multiplier to get 90-th percentile
s90 = 1.6448536269514729



def fig2(w, h, left=0.047, bottom=0.035, right=0.99, top=0.99, wspace=None,
         hspace=1.0):
    """
    Figure 2: All data
    """
    fig = plt.figure(figsize=(w, h))
    fig.subplots_adjust(left, bottom, right, top)
    grid = fig.add_gridspec(6, 2, wspace=wspace, hspace=hspace)
    ax1 = fig.add_subplot(grid[:-1, :])
    ax31 = fig.add_subplot(grid[-1, 0])
    ax32 = fig.add_subplot(grid[-1, 1])

    # Gather data
    with base.connect() as con:
        c = con.cursor()

        qand = ' and cell != "Oocyte"'
        q = ('select vi, semi, stdi, ni from midpoints_wt'
             f' where ni > 0 {qand} order by vi')
        i = [row for row in c.execute(q)]
        q = ('select va, sema, stda, na from midpoints_wt'
             f' where na > 0 {qand} order by va')
        a = [row for row in c.execute(q)]

    #
    # Top: all data
    #
    xlim = -120, 0
    ax1.set_xlabel('Membrane potential (mV)')
    ax1.set_xlim(*xlim)
    ax1.set_ylim(-2, 1 + max(len(a), len(i)))
    for s in ax1.spines.values():
        s.set_visible(False)
    ax1.spines['bottom'].set_visible(True)
    ax1.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(20))
    ax1.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
    ax1.get_yaxis().set_visible(False)
    ax1.grid(ls='--', color='#cccccc', zorder=0)

    sstd = dict(color='#999')
    ssem = dict(color='k', lw=3.8)
    ca = 'tab:blue'
    ci = 'tab:orange'
    m = 'o'
    ms = 4

    offset = max(0, (len(a) - len(i)) / 2)
    for k, d in enumerate(i):
        mu, sem, std, n = d

        k += offset
        ax1.plot((mu - s90 * std, mu + s90 * std), (k, k), **sstd, zorder=2)
        ax1.plot((mu - sem, mu + sem), (k, k), **ssem, zorder=3)
        ax1.plot(mu, k, m, color=ci, markersize=ms, zorder=4)

    offset = max(0, (len(i) - len(a)) / 2)
    for k, d in enumerate(a):
        mu, sem, std, n = d

        ax1.plot((mu - s90 * std, mu + s90 * std), (k, k), **sstd, zorder=2)
        ax1.plot((mu - sem, mu + sem), (k, k), **ssem, zorder=3)
        ax1.plot(mu, k, m, color=ca, markersize=ms, zorder=4)

    ms2 = 12
    elements = [
        matplotlib.lines.Line2D(
            [0], [0], marker=m, color='w', label=r'$\mu_i$', markersize=ms2,
            markerfacecolor=ci),
        matplotlib.lines.Line2D(
            [0], [0], marker=m, color='w', label=r'$\mu_a$', markersize=ms2,
            markerfacecolor=ca),
        matplotlib.lines.Line2D(
            [0], [0], color=ssem['color'], label='SEM', lw=ssem['lw']),
        matplotlib.lines.Line2D(
            [0], [0], color=sstd['color'], label='5th-95th percentile'),
    ]
    ax1.legend(loc='upper left', frameon=False, handles=elements)

    #
    # Bottom: Histogram of sigma and of n
    #
    vi, _, stdi, ni = np.array([row for row in i]).T
    va, _, stda, na = np.array([row for row in a]).T


    ax31.set_xlabel(r'$\sigma$ (mV)')
    ax31.set_ylabel('Percentage')
    ax31.set_xlim(-1, 24)
    ax31.set_ylim(0, 23)
    top90 = lambda sigma: sigma * s90 * 2
    frp90 = lambda p90: p90 / (s90 * 2)
    ax31t = ax31.secondary_xaxis('top', functions=(top90, frp90))
    ax31t.set_xlabel('5th-95th percentile range (mV)')

    bins = np.arange(0, 24, 1)
    kwargs = dict(bins=bins, facecolor='none')
    w = np.ones(len(stdi)) / len(stdi) * 100
    ax31.hist(stdi, weights=w, edgecolor='tab:orange', label=r'$\sigma_i$',
              **kwargs)
    w = np.ones(len(stda)) / len(stda) * 100
    ax31.hist(
        stda, weights=w, edgecolor='tab:blue', label=r'$\sigma_a$', **kwargs)
    ax31.legend(loc='upper right', frameon=False)

    ax32.set_xlabel('n')
    ax32.set_ylabel('Percentage')
    ax32.set_xlim(1, 90)

    bins = np.arange(1, 90, 2)
    kwargs = dict(bins=bins, facecolor='none')
    w = np.ones(len(stdi)) / len(stdi) * 100
    ax32.hist(ni, weights=w, edgecolor='tab:orange', label=r'$n_i$', **kwargs)
    w = np.ones(len(stda)) / len(stda) * 100
    ax32.hist(na, weights=w, edgecolor='tab:blue', label=r'$n_a$', **kwargs)
    ax32.legend(loc='upper right', frameon=False)

    return fig


def fig3(w, h, left=0.14, bottom=0.09, right=0.99, top=0.99):
    """
    Figure 3: Correlation
    """
    fig = plt.figure(figsize=(w, h))
    fig.subplots_adjust(left, bottom, right, top)
    ax = fig.add_subplot()

    xlim = -65, -15
    ylim = -112, -58
    # NOTE: These measurements chosen to get almost equal aspect manually

    c1 = 'tab:orange'
    c2 = 'tab:red'

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

        qand = 'and cell != "Oocyte"'
        q = ('select pub, va, stda, vi, stdi, na, ni from midpoints_wt'
             f' where (na > 0 and ni > 0 {qand})')
        d_all = get(q)
        n_all = len(d_all[0])

    # Extract va and vi
    va, vi = np.array(d_all[1]), np.array(d_all[2])

    # Fit line
    p1 = np.corrcoef(va, vi)[1, 0]
    b1, a1 = np.polyfit(va, vi, 1)
    mu_a, mu_i = np.mean(va), np.mean(vi)


    def ci_linear_1d(x, y, alpha=95):
        x, y = np.asarray(x), np.asarray(y)

        b, a = np.polyfit(x, y, 1)
        n = len(x)  # Number of observations
        m = 2       # Number of parameters
        d = n - m   # Degrees of freedom

        # For a 90% interval we need to use 0.975
        # See e.g. https://en.wikipedia.org/wiki/Confidence_interval#Example
        alpha = (100 - alpha) / 100     # Turn 95 into 0.05
        alpha = 1 - alpha / 2
        t = scipy.stats.t.ppf(alpha, n - m)

        # Residuals
        r = y - (a + b * x)
        s = np.sqrt(np.sum(r**2) / d)   # Standard deviation of the residuals

        # Mean, and other fixed terms
        mu = np.mean(x)
        ts = t * s
        ni = 1 / n
        di = 1 / np.sum((x - mu)**2)
        return lambda z: ts * np.sqrt(ni + (z - mu)**2 * di)


    # Fit line with slope of 1
    a2 = np.polyfit(va, vi - va, 0)[0]
    b2 = 1

    ax.set_xlabel(r'$\mu_a$ (mV)')
    ax.set_ylabel(r'$\mu_i$ (mV)')
    ax.grid(True, ls=':')
    ax.set(xlim=xlim, ylim=ylim)
    #ax.axis('equal')  This changes the limits

    # Projections / orthogonal
    a, b = a1, b1

    # Mean x and y, projected onto line (should stay the same!)
    ma, mi = np.mean(va), np.mean(vi)
    f = (ma + (mi - a) * b) / (1 + b * b)
    mx, my = f, a + f * b

    # Project all points onto fit, then get tangential and orthogonal length
    d1s = ((va - mx) + b * (vi - my)) / np.sqrt(1 + b**2)
    d2s = ((vi - my) - b * (va - mx)) / np.sqrt(1 + b**2)

    # Plot linear fit
    l1_color = 'tab:blue'
    x = np.array(xlim)
    l1 = ax.plot(x, a1 + b1 * x, '-', color=l1_color,
                 label=f'{a1:.1f} mV + {b1:.2f} $V_a$')

    # Plot confidence infterval
    x = np.linspace(xlim[0], xlim[1], 100)
    ci = ci_linear_1d(va, vi)
    l2 = ax.plot(x, a1 + b1 * x + ci(x), '--', color=l1_color,
                 label='95% confidence interval')
    ax.plot(x, a1 + b1 * x - ci(x), '--', color=l1_color)
    ax.fill_between(x, a1 + b1 * x + ci(x), a1 + b1 * x - ci(x), color='#ddd')

    # Plot fixed-slope fit
    l3 = ax.plot(x, a2 + b2 * x, '-', color='tab:green',
                 label=f'{a2:.1f} mV + {b2:.2f} $V_a$')

    # Plot midpoints
    m = 'o'
    ax.plot(d_all[1], d_all[2], m, color='k', markerfacecolor='w')

    # Mean
    mean = ax.plot(
        mu_a, mu_i, '*', color='yellow', lw=5, markersize=15,
        markeredgecolor='k', markeredgewidth=1, label='mean', zorder=4)

    # Custom legend
    def l2d(**kwargs):
        return matplotlib.lines.Line2D([0], [0], **kwargs)


    ms2 = 12
    elements = []
    elements.append(l2d(marker=m, color='k', ls='none', markerfacecolor='w',
                        label=f'Experiments ({len(d_all[1])})'))
    elements.append(l2d(marker='*', ls='none', color='yellow', markersize=11,
                        markeredgecolor='k', label='Mean-of-means'))
    elements.append(l1[0])
    elements.append(l2[0])
    elements.append(l3[0])

    ax.legend(loc='lower right', handles=elements, framealpha=1, fontsize=9)

    return fig


def fig4(w, h, left=0.045, bottom=0.15, right=0.955, top=0.86, wspace=None):
    """
    Figure 4: subgroups
    """
    fig = plt.figure(figsize=(w, h))
    fig.subplots_adjust(left, bottom, right, top)
    grid = fig.add_gridspec(1, 6, wspace=wspace)
    ax11 = fig.add_subplot(grid[0, 0])
    ax12 = fig.add_subplot(grid[0, 1])
    ax13 = fig.add_subplot(grid[0, 2])
    ax21 = fig.add_subplot(grid[0, 3])
    ax22 = fig.add_subplot(grid[0, 4])
    ax23 = fig.add_subplot(grid[0, 5])

    xlim = -62, -19
    ylim = -109, -59
    # NOTE: These measurements picked to manually give axes equal aspect

    # Gather data
    with base.connect() as con:
        c = con.cursor()

        qand = 'and cell != "Oocyte"'
        q = ('select va, vi, sequence, beta1, cell, pub from midpoints_wt'
             f' where (ni > 0 and na > 0 {qand})')
        p = [row for row in c.execute(q)]

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

    ax11.set_xlabel(r'$\mu_a$ (mV)')
    ax11.set_ylabel(r'$\mu_i$ (mV)')
    ax11.grid(True, ls=':')
    ax11.set_xlim(*xlim)
    ax11.set_ylim(*ylim)

    ax12.set_xlabel(r'$\mu_a$ (mV)')
    ax12.set_yticklabels([])
    ax12.grid(True, ls=':')
    ax12.set_xlim(*xlim)
    ax12.set_ylim(*ylim)

    ax13.set_xlabel(r'$\mu_a$ (mV)')
    ax13.set_yticklabels([])
    ax13.grid(True, ls=':')
    ax13.set_xlim(*xlim)
    ax13.set_ylim(*ylim)

    ax21.set_xlabel(r'$\mu_a$ (mV)')
    ax21.set_yticklabels([])
    ax21.grid(True, ls=':')
    ax21.set_xlim(*xlim)
    ax21.set_ylim(*ylim)

    ax22.set_xlabel(r'$\mu_a$ (mV)')
    ax22.set_yticklabels([])
    ax22.grid(True, ls=':')
    ax22.set_xlim(*xlim)
    ax22.set_ylim(*ylim)

    ax23.set_xlabel(r'$\mu_a$ (mV)')
    ax23.set_ylabel(r'$\mu_i$ (mV)')
    ax23.yaxis.set_label_position('right')
    ax23.yaxis.tick_right()
    ax23.grid(True, ls=':')
    ax23.set_xlim(*xlim)
    ax23.set_ylim(*ylim)

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

    return fig


#
# Create figure
#
print('Creating figures')

r = 0.02
#fig2(524 * r, 632 * r).savefig('poster-2.svg')
#fig3(259 * r, 257 * r).savefig('poster-3.svg')
fig4(815 * r, 161 * r).savefig('poster-4.svg')

