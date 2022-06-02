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

