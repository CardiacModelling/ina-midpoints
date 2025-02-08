#!/usr/bin/env python3
#
# Calculates statistics about the means reported in the midpoints data.
#
import numpy as np

import base

nooocytes = True
qand = ' and cell != "Oocyte" group by pub'

# Query db
with base.connect() as con:
    c = con.cursor()
    def g(x):
        q = f'select {x} from midpoints_wt where {x} is not null {qand}'
        return np.array([row[x] for row in c.execute(q)])
    ah, alo, da, ahi = g('pah'), g('palo'), g('pad'), g('pahi')
    ih, ilo, di, ihi, it = g('pih'), g('pilo'), g('pid'), g('pihi'), g('pit')


def occs(name, x):
    v, c = np.unique(x, return_counts=True)
    print(f'{name:<9}'
          + ' '.join([f'{x:^4}' for x in v]) + '\n' + ' '*9
          + ' '.join([f'{x:^4}' for x in c]))
    return v[np.argmax(c)]


# Calculate
print('Activation protocol')
a = occs('V hold', ah)
b = occs('V low', alo)
c = occs('V step', da)
d = occs('V high', ahi)
print(f'Modal protocol: hold at {a}, step from {b} to {d} in {c}mV steps')
with base.connect() as con:
    r = con.cursor()
    q = (f'select pah from midpoints_wt where pah == {a} and palo == {b} and'
         f' pad == {c} and pahi == {d} {qand}')
    n = len([row for row in r.execute(q)])
    print(f' exact modal occurs: {n} times')
    q = (f'select palo from midpoints_wt where palo == {b} and pahi == {d}'
         f' and pad == {c} {qand}')
    n = len([row for row in r.execute(q)])
    print(f' low/high/step combo occurs: {n} times')
    q = (f'select pub from midpoints_wt where palo == {b} and pahi == {d}'
         f' {qand}')
    rows = [row['pub'] for row in r.execute(q)]
    print(f' low/high combo occurs: {len(rows)} times:')
    for r in rows:
        print(f'    {r}')

print('Inactivation protocol')
a = occs('V hold', ih)
b = occs('V low', ilo)
c = occs('V step', di)
d = occs('V high', ihi)
e = occs('V test', it)
print(f'Modal protocol: hold at {a}, step from {b} to {d} in {c}mV steps,'
      f' test at {e}mV')
with base.connect() as con:
    r = con.cursor()
    q = (f'select pih from midpoints_wt where pih == {a} and pilo == {b} and'
         f' pid == {c} and pihi == {d} and pit == {e} {qand}')
    n = len([row for row in r.execute(q)])
    print(f' exact modal occurs: {n} times')
    q = (f'select pih from midpoints_wt where pilo == {b} and pihi == {d} and'
         f' pid == {c} and pit == {e} {qand}')
    n = len([row for row in r.execute(q)])
    print(f' low/high/step/test combo occurs: {n} times')
    q = (f'select pih from midpoints_wt where pilo == {b} and pihi == {d} and'
         f' pid == {c} {qand}')
    n = len([row for row in r.execute(q)])
    print(f' low/high/step combo occurs: {n} times')
    q = (f'select pih from midpoints_wt where pilo == {b} and pihi == {d} and'
         f' pit == {e} {qand}')
    n = len([row for row in r.execute(q)])
    print(f' low/high/test combo occurs: {n} times')
    q = (f'select pub from midpoints_wt where pilo == {b} and pihi == {d}'
         f' {qand}')
    rows = [row['pub'] for row in r.execute(q)]
    print(f' low/high combo occurs: {len(rows)} times:')
    for r in rows:
        print(f'    {r}')

