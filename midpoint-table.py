#!/usr/bin/env python3
#
# Create a TeX table of all reported midpoints.
#
import base

filename = 'midpoint-table.tex'

# Collect journal references
refs = {}
with base.connect() as con:
    c = con.cursor()
    q = 'select key, tex from publication_tex'
    for k, row in enumerate(c.execute(q)):
        refs[row['key']] = row['tex']

# Create table file
fields = [
    'pub',
    'va',
    'na',
    'stda',
    'vi',
    'ni',
    'stdi',
    'sequence',
    'cell',
    'beta1',
]

# Sequence formatting
def seq(s):
    if s == 'astar':
        return 'a*'
    elif s == 'bstar':
        return 'b*'
    elif s is None:
        return '?'
    return s

# Create table
print(f'Writing to {filename}...')
with open(filename, 'w') as f:
    # Header
    size = 'footnotesize'
    f.write('\\begin{' + size + '}\n')
    f.write('\\startrowcolors\n')
    f.write('\\begin{longtable}{p{5cm}|lll|lll|lll}\n')
    f.write('\\caption{\\label{midpoints}Midpoints} \\\\\n')
    f.write('\\hline\n')
    f.write('Publication')
    f.write(' & $V_a$ & $\sigma_a$  & $n_a$')
    f.write(' & $V_i$ & $\sigma_i$  & $n_i$')
    f.write(' & Cell & $\\alpha$ & $\\beta1$ \\\\\n')
    f.write('\\hline\n')
    f.write('\\endfirsthead')
    f.write('\\hline\n')
    f.write('\\rowcolor{white}\n')
    f.write('Publication')
    f.write(' & $V_a$ & $\sigma_a$  & $n_a$')
    f.write(' & $V_i$ & $\sigma_i$  & $n_i$')
    f.write(' & Cell & $\\alpha$ & $\\beta1$ \\\\\n')
    f.write('\\hline\n')
    f.write('\\endhead\n')
    f.write('\\hline\n')
    f.write('\\endfoot\n')
    # Body
    form = '{:.3g}'
    with base.connect() as con:
        c = con.cursor()
        q = 'select ' + ', '.join(fields) + ' from midpoints_wt'
        for k, row in enumerate(c.execute(q)):
            x = []
            x.append('\\citet{' + refs[row['pub']] + '}')
            if row['na'] != 0:
                x.append(form.format(row['va']))
                x.append(form.format(row['stda']))
                x.append(form.format(row['na']))
            else:
                x.append('&&')
            if row['ni'] != 0:
                x.append(form.format(row['vi']))
                x.append(form.format(row['stdi']))
                x.append(form.format(row['ni']))
            else:
                x.append('&&')
            x.append(row['cell'].replace('Oocyte', 'Ooc.'))
            x.append(seq(row['sequence']))
            x.append(row['beta1'])
            f.write(' & '.join(x) + ' \\\\\n')
    # Footer
    f.write('\\end{longtable}\n')
    f.write('\\end{' + size + '}\n')
print('Done.')
