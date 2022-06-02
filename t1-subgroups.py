#!/usr/bin/env python3
#
# Creates a table of statistics about the total data and all subgroups.
#
import os

import base


def midpoints_wt(con):
    """
    Create summed PDFs of midpoint data for WT expression system experiments.
    """
    c = con.cursor()
    rows = []

    def do(name, query):
        rows.append((name, ) + base.combined_pdf(c.execute(query))[1:])

    # All data
    a = 'select pub, va, sema, na, stda from midpoints_wt'
    i = 'select pub, vi, semi, ni, stdi from midpoints_wt'
    do('Act; Combined', a)
    do('Inact; Combined', r)

    # HEK, a*, beta1
    r = ' where sequence == "astar" and cell == "HEK" and beta1 == "yes"'
    do('Act; Common'a + r)
    do('Inact; Common'i + r)

    # Isoform a
    r = ' where sequence == "a"'
    do('Act; Isoform a'a + r)
    do('Inact; Isoform a'i + r)

    # Isoform b
    r = ' where sequence == "b"'
    do('Act; Isoform b'a + r)
    do('Inact; Isoform b'i + r)

    # Isoform a*
    r = ' where sequence == "astar"'
    do('Act; Isoform a*'a + r)
    do('Inact; Isoform a*'i + r)

    # Isoform b*
    r = ' where sequence == "bstar"'
    do('Act; Isoform b*'a + r)
    do('Inact; Isoform b*'i + r)

    # Isoform unknown
    r = ' where sequence is null'
    do('Act; Isoform ?'a + r)
    do('Inact; Isoform ?'i + r)

    # With beta1
    r = ' where beta1 == "yes"'
    do('Act; With beta1'a + r)
    do('Inact; With beta1'i + r)

    # Without beta1
    r = ' where beta1 == "no"'
    do('Act; Without beta1'a + r)
    do('Inact; Without beta1'i + r)

    # HEK
    r = ' where cell == "HEK"'
    do('Act; HEK'a + r)
    do('Inact; HEK'i + r)

    # CHO
    r = ' where cell == "CHO"'
    do('Act; CHO'a + r)
    do('Inact; CHO'i + r)

    # Oocytes
    r = ' where cell == "Oocyte"'
    do('Act; Oocyte'a + r)
    do('Inact; Oocyte'i + r)

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
    wt = midpoints_wt(con)

    # Show tables
    head = ['', 'reports', 'cells', 'mean', 'stddev', 'lo', 'hi', 'p']
    print()
    base.table(head, wt)
    print()


    # Write partial tex table
    tex_table_wt(wt, 't1-subgroups.tex')

