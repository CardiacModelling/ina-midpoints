#!/usr/bin/env python3
#
# Creates data for a graph of V1/2 of activation & inactivation of wild-type
# channels in expression systems and myocyte data.
#
# Also writes t1-midpoints.tex
#
import os

import numpy as np
import scipy.stats

import base


def gaussian(x, mu, sigma):
    """
    Return a gaussian/normal pdf over x, with mean mu and stddev sigma.
    """
    return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(
        -np.power((x - mu) / sigma, 2) * 0.5)


def gather(filename, rows, write_individual=False):
    """
    Gathers data from the provided ``rows``, calculates a combined PDF, and
    writes it to a CSV file ``filename``.

    Each row must contain five columns in the order ``(name, v, sem, n, std)``.
    The resulting PDF is written to a CSV file

    The CSV file ``filename`` will contain the columns ``x``, ``sum`` and
    ``gauss``, containing x coordinates, the summed-andeighted PDF, and a
    Gaussian approximation, respectively.
    If ``write_individual`` is ``True``, this will be followed by a list of
    PDFs for each of the individual rows.

    Returns a list ``[m, n, mean, sigma, lo, hi, p]``, where ``m`` is
    the number of reports, ``n`` is the total number of cells, ``area`` is the
    area under the constructed PDF, ``mean`` and ``sigma`` are the mean and
    standard deviation of the PDF, ``lo`` and ``hi`` are the lower and upper
    bounds of the 2-sigma range, and ``p`` is the p-value from a chi-squared
    test testing if the PDF is normal.
    """
    # High number of x-axis points, for accurate calculations
    npoints = 100000

    # Lower number of points, for fast representations
    xf = int(npoints // 1000)

    # Create x-data and y-data
    x = np.linspace(-140, 20, npoints)
    y = np.zeros(x.shape)

    # Names of each measurement
    fields = []
    # Result for each measurement (v, std, n)
    data = {}
    # Total number of cells measured
    ntotal = 0

    # Gather data from rows
    for k, row in enumerate(rows):
        pub, v, sem, n, std = row
        field = str(k) + '-' + pub
        # Skip rows without act/inact measurement
        if n == 0:
            continue
        # Check std calculation
        if np.abs(std - sem * np.sqrt(n)) > 1e-6:
            print(f'Warning: Error in STD for {field}')
            print(f'  Listed    : {std}')
            print(f'  Calculated: {sem * np.sqrt(n)}')
        # Update ntotal
        ntotal += n
        # Store data
        fields.append(field)
        data[field] = (v, std, n)

    # Create probability density functions
    nmeasurements = len(fields)
    pdfs = {}
    for field in fields:
        v, std, n = data[field]

        # Create pdf, weighted by n / ntotal
        pdf = (n / ntotal) * gaussian(x, v, std)

        # Update sum
        y += pdf

        # Store reduced data
        if write_individual:
            pdfs[field] = pdf[::xf]

    # Calculate mean and standard deviation
    mu = np.sum(x * y) / np.sum(y)
    sigma = np.sqrt(np.sum(y * ((x - mu) ** 2)) / np.sum(y))

    # Test goodness of fit using a chi-squared test
    z = gaussian(x, mu, sigma)
    chisq, p = scipy.stats.chisquare(
        y / np.sum(y),
        z / np.sum(z),
        2,  # 2 params used to estimate z
    )

    # Area under PDF
    # print(f'Area under PDF: {np.sum(y) * (x[1] - x[0])}')

    # Reduce data
    x = x[::xf]
    y = y[::xf]

    # Draw gaussian curve
    z = gaussian(x, mu, sigma)

    # Ignore individual results, if not wanted
    if not write_individual:
        fields = []

    # Write file
    path = os.path.join(base.DIR_DATA_OUT, filename)
    print(f'Writing to {os.path.relpath(path)}')
    with open(path, 'w') as f:
        csv = base.csv_writer(f)
        csv.writerow(['x', 'sum', 'gauss'] + fields)
        data = [iter(x), iter(y), iter(z)] + [iter(pdfs[f]) for f in fields]
        for i in range(len(x)):
            csv.writerow([next(j) for j in data])

    # Return (m, n, area, mean, sigma, lo, hi, p)
    lo = mu - 2 * sigma
    hi = mu + 2 * sigma
    return [nmeasurements, int(ntotal), mu, sigma, lo, hi, p]


def midpoints_wt(con):
    """
    Create summed PDFs of midpoint data for WT expression system experiments.
    """
    c = con.cursor()
    rows = []

    # All data
    a = 'select pub, va, sema, na, stda from midpoints_wt'
    i = 'select pub, vi, semi, ni, stdi from midpoints_wt'
    filename = 'midpoints-wt-a-00-all.csv'
    rows.append(['Act; Combined'] + gather(filename, c.execute(a)))
    filename = 'midpoints-wt-i-00-all.csv'
    rows.append(['Inact; Combined'] + gather(filename, c.execute(i)))

    # HEK, a*, beta1
    r = ' where sequence == "astar" and cell == "HEK" and beta1 == "yes"'
    filename = 'midpoints-wt-a-11-most-common.csv'
    rows.append(['Act; Common'] + gather(filename, c.execute(a + r)))
    filename = 'midpoints-wt-i-11-most-common.csv'
    rows.append(['Inact; Common'] + gather(filename, c.execute(i + r)))

    # Isoform a
    r = ' where sequence == "a"'
    filename = 'midpoints-wt-a-01-isoform-a.csv'
    rows.append(['Act; Isoform a'] + gather(filename, c.execute(a + r)))
    filename = 'midpoints-wt-i-01-isoform-a.csv'
    rows.append(['Inact; Isoform a'] + gather(filename, c.execute(i + r)))

    # Isoform b
    r = ' where sequence == "b"'
    filename = 'midpoints-wt-a-02-isoform-b.csv'
    rows.append(['Act; Isoform b'] + gather(filename, c.execute(a + r)))
    filename = 'midpoints-wt-i-02-isoform-b.csv'
    rows.append(['Inact; Isoform b'] + gather(filename, c.execute(i + r)))

    # Isoform a*
    r = ' where sequence == "astar"'
    filename = 'midpoints-wt-a-03-isoform-a-star.csv'
    rows.append(['Act; Isoform a*'] + gather(filename, c.execute(a + r)))
    filename = 'midpoints-wt-i-03-isoform-a-star.csv'
    rows.append(['Inact; Isoform a*'] + gather(filename, c.execute(i + r)))

    # Isoform b*
    r = ' where sequence == "bstar"'
    filename = 'midpoints-wt-a-04-isoform-b-star.csv'
    rows.append(['Act; Isoform b*'] + gather(filename, c.execute(a + r)))
    filename = 'midpoints-wt-i-04-isoform-b-star.csv'
    rows.append(['Inact; Isoform b*'] + gather(filename, c.execute(i + r)))

    # Isoform unknown
    r = ' where sequence is null'
    filename = 'midpoints-wt-a-05-isoform-unknown.csv'
    rows.append(['Act; Isoform ?'] + gather(filename, c.execute(a + r)))
    filename = 'midpoints-wt-i-05-isoform-unknown.csv'
    rows.append(['Inact; Isoform ?'] + gather(filename, c.execute(i + r)))

    # With beta1
    r = ' where beta1 == "yes"'
    filename = 'midpoints-wt-a-09-with-beta1.csv'
    rows.append(['Act; With beta1'] + gather(filename, c.execute(a + r)))
    filename = 'midpoints-wt-i-09-with-beta1.csv'
    rows.append(['Inact; With beta1'] + gather(filename, c.execute(i + r)))

    # Without beta1
    r = ' where beta1 == "no"'
    filename = 'midpoints-wt-a-10-without-beta1.csv'
    rows.append(['Act; Without beta1'] + gather(filename, c.execute(a + r)))
    filename = 'midpoints-wt-i-10-without-beta1.csv'
    rows.append(['Inact; Without beta1'] + gather(filename, c.execute(i + r)))

    # HEK
    r = ' where cell == "HEK"'
    filename = 'midpoints-wt-a-06-hek.csv'
    rows.append(['Act; HEK'] + gather(filename, c.execute(a + r)))
    filename = 'midpoints-wt-i-06-hek.csv'
    rows.append(['Inact; HEK'] + gather(filename, c.execute(i + r)))

    # CHO
    r = ' where cell == "CHO"'
    filename = 'midpoints-wt-a-08-cho.csv'
    rows.append(['Act; CHO'] + gather(filename, c.execute(a + r)))
    filename = 'midpoints-wt-i-08-cho.csv'
    rows.append(['Inact; CHO'] + gather(filename, c.execute(i + r)))

    # Oocytes
    r = ' where cell == "Oocyte"'
    filename = 'midpoints-wt-a-07-oocytes.csv'
    rows.append(['Act; Oocyte'] + gather(filename, c.execute(a + r)))
    filename = 'midpoints-wt-i-07-oocytes.csv'
    rows.append(['Inact; Oocyte'] + gather(filename, c.execute(i + r)))

    return rows


def midpoints_myo(con):
    """
    Create summed PDFs of midpoint data for human myocyte experiments.
    """
    c = con.cursor()
    rows = []

    q = 'select pub, va, sema, na, stda from midpoints_myo'
    filename = 'midpoints-myo-a-00-all.csv'
    rows.append(['Act; myocytes'] + gather(filename, c.execute(q), True))
    q = 'select pub, vi, semi, ni, stdi from midpoints_myo'
    filename = 'midpoints-myo-i-00-all.csv'
    rows.append(['Inact; myocytes'] + gather(filename, c.execute(q), True))

    return rows


def tex_table_wt(rows, filename):

    # Turn rows into dict
    data = {}
    for row in rows:
        data[row[0]] = row[1:]

    def row(f, key, fancyname=None):
        if not fancyname:
            fancyname = key

        # Convert a table row to a tex table row
        #        0           1     2    3    4   5   6
        # [nmeasurements, ntotal, mu, sigma, lo, hi, p]
        a = data['Act; ' + key]
        b = data['Inact; ' + key]
        return ' & '.join((
            fancyname,
            f'{a[2]:3.3g}',
            f'{a[3]:3.3g}',
            f'{a[4]:3.3g}, {a[5]:3.3g}',
            str(a[0]),
            str(a[1]),
            f'{b[2]:3.3g}',
            f'{b[3]:3.3g}',
            f'{b[4]:3.3g}, {b[5]:3.3g}',
            str(b[0]),
            str(b[1]),
        )) + r' \\' + '\n'

    # Build table
    print(f'Writing table to {filename}')
    with open(filename, 'w') as f:
        f.write(r'\begin{tabular}{l | lll | cc | lll | cc}' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\multicolumn{1}{l|}{}')
        f.write(r' & \multicolumn{5}{l|}{Activation}')
        f.write(r' & \multicolumn{5}{l}{Inactivation} \\ \hline' + '\n')
        f.write(r'{} & $\mu_a$ & $\sigma_a$ & $r_{2\sigma,a}$ & m & n' + '\n')
        f.write(r'   & $\mu_i$ & $\sigma_i$ & $r_{2\sigma,i}$ & m & n')
        f.write(r' \\ \hline' + '\n')

        f.write(row(f, 'Combined'))
        f.write(row(f, 'Common', r'HEK, a*, \bet1'))
        f.write('\hline\n')
        f.write(row(f, 'Isoform a'))
        f.write(row(f, 'Isoform b'))
        f.write(row(f, 'Isoform a*'))
        f.write(row(f, 'Isoform b*'))
        f.write(row(f, 'Isoform ?', 'Unknown'))
        f.write('\hline\n')
        f.write(row(f, 'With beta1', r'With \bet1'))
        f.write(row(f, 'Without beta1', r'Without \bet1'))
        f.write('\hline\n')
        f.write(row(f, 'HEK'))
        f.write(row(f, 'CHO'))
        f.write(row(f, 'Oocyte'))

        f.write(r'\hline' + '\n')
        f.write(r'\end{tabular}' + '\n')


with base.connect() as con:
    myo = midpoints_myo(con)
    wt = midpoints_wt(con)

    # Show tables
    head = ['', 'reports', 'cells', 'mean', 'stddev', 'lo', 'hi', 'p']
    print()
    base.table(head, myo)
    print()
    base.table(head, wt)
    print()

    # Write partial tex table
    tex_table_wt(wt, 't1-subgroups.tex')

