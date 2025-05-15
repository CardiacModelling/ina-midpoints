#!/usr/bin/env python3
#
# Calculates statistics about the standard deviations reported in the midpoints
# data.
#
import numpy as np

import base

filename = 't2-cell-counts.tex'
nooocytes = True

a = 'and cell != "Oocyte"' if nooocytes else ''
with base.connect() as con:
    c = con.cursor()

    # Get difference in na and ni for all experiments reporting both
    q = f'select na, ni from midpoints_wt where na > 0 and ni > 0 {a}'
    rows = [row for row in c.execute(q)]
    nani = [int(abs(row[1] - row[0])) for row in rows]
    n = len(nani)

    counts, bins = np.histogram(nani, bins=sorted(set(nani)))
    del rows, nani

# Calculate percentages and cumulative percentages
percentages = np.round(100 * counts / n, 1)
cumulative = np.round(100 * np.cumsum(counts) / n, 1)

# Caption, with example
i = 3
caption = rf"""
A `histogram' view of the difference in cell counts ($|n_a - n_i|$) and how
often each was encountered.
The third column gives the number of occurrences as a percentage, and the
final column provides the cumulative percentage (e.g. {cumulative[i]}\% of
experiments had an $|n_a - n_i| \leq {bins[i]}$).
""".strip()

print(f'Writing to {filename}...')
with open(filename, 'w') as f:
    # Head
    eol = '\n'
    f.write(r'\startrowcolors' + eol)
    f.write(r'\begin{longtable}{l|l|l|l}' + eol)
    f.write(r'\caption{' + caption + r'} \\' + eol)
    f.write(r'\hline' + eol)
    f.write(r'\rowcolor{white}' + eol)
    f.write(r'$|n_a - n_i|$')
    f.write(r' & Number of occurrences')
    f.write(r' & Percentage')
    f.write(r' & Cumulative percentage')
    f.write(r'\\ \hline' + eol)
    f.write(r'\endfirsthead' + eol)
    f.write(r'\hline' + eol)
    f.write(r'\rowcolor{white}' + eol)
    f.write(r'$|n_a - n_i|$')
    f.write(r' & Number of occurrences')
    f.write(r' & Percentage')
    f.write(r' & Cumulative percentage')
    f.write(r'\\ \hline' + eol)
    f.write(r'\endhead' + eol)
    f.write(r'\hline' + eol)
    f.write(r'\endfoot' + eol)

    # Body
    for b, c, p, q in zip(bins, counts, percentages, cumulative):
        f.write(rf'{b:2d} & {c:2d} & {p:>4.1f}\% & {q:>5.1f}\% \\{eol}')

    # Footer
    f.write(r'\end{longtable}' + eol)

print('Done.')
