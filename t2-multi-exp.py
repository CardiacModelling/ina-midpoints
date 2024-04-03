#!/usr/bin/env python3
#
# Calculates max between exp var in Kapplinger and Tan
#
import base

filename = 't2-multi-exp.tex'
nooocytes = True

qo = 'where cell != "Oocyte"' if nooocytes else ''

# Collect journal references
refs = {}
with base.connect() as con:
    c = con.cursor()
    q = 'select key, tex from publication_tex'
    for k, row in enumerate(c.execute(q)):
        refs[row['key']] = row['tex']


print(f'Writing to {filename}...')
with open(filename, 'w') as f:
    # Head
    eol = '\n'
    f.write(r'\startrowcolors' + eol)
    f.write(r'\begin{longtable}{p{6cm}|l}' + eol)
    f.write(r'\hline' + eol)
    f.write(r'\rowcolor{white}' + eol)
    f.write(r'Publication')
    f.write(r' & Number of experiments')
    f.write(r'\\ \hline' + eol)
    f.write(r'\endfirsthead' + eol)
    f.write(r'\hline' + eol)
    f.write(r'\rowcolor{white}' + eol)
    f.write(r'Publication')
    f.write(r' & Number of experiments')
    f.write(r'\\ \hline' + eol)
    f.write(r'\endhead' + eol)
    f.write(r'\hline' + eol)
    f.write(r'\endfoot' + eol)

    # Body
    form = '{:.3g}'
    with base.connect() as con:
        c = con.cursor()
        rows = c.execute(f'select pub, count(*) as c from midpoints_wt {qo}'
                         ' group by pub having c > 1 order by c desc;')
        for row in rows:
            x = []
            x.append(r'\citet{' + refs[row['pub']] + '}')
            x.append(form.format(row['c']))
            f.write(' & '.join(x) + r' \\' + eol)

    # Footer
    f.write(r'\end{longtable}' + eol)

print('Done.')
