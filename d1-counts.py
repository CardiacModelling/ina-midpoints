#!/usr/bin/env python3
#
# Calculates statistics about the standard deviations reported in the midpoints
# data.
#
import base

nooocytes = True

if nooocytes:
    w = 'where cell != "Oocyte"'
    a = 'and cell != "Oocyte"'
else:
    w = a = ''

with base.connect() as con:
    c = con.cursor()

    # Count total number of reports (1 or more per publication)
    row = next(c.execute(f'select count(pub) from midpoints_wt {w}'))
    print(f'Total experiments: {row[0]}')

    # Count total number of publications
    row = next(c.execute(f'select count(distinct(pub)) from midpoints_wt {w}'))
    print(f'Total studies: {row[0]}')

    # Count Va measurements
    print()
    row = next(c.execute(
        f'select count(va) from midpoints_wt where na > 0 {a}'))
    print(f'Total Va experiments: {row[0]}')

    # Count Vi measurements
    row = next(c.execute(
        f'select count(vi) from midpoints_wt where ni > 0 {a}'))
    print(f'Total Vi experiments: {row[0]}')

    # Count Va + Vi measurements
    print()
    row = next(c.execute(
        f'select count(vi) from midpoints_wt where na > 0 and ni > 0 {a}'))
    print(f'Total Va+Vi experiments: {row[0]}')
    row = next(c.execute(
        f'select count(vi) from midpoints_wt where na > 0 and ni == 0 {a}'))
    print(f'Va-only experiments: {row[0]}')
    row = next(c.execute(
        f'select count(vi) from midpoints_wt where ni > 0 and na == 0 {a}'))
    print(f'Vi-only experiments: {row[0]}')

    # Cell count
    print()
    row = next(c.execute(f'select sum(na), sum(ni) from midpoints_wt {w}'))
    print(f'Total cells act: {int(row[0])}')
    print(f'Total cells inact: {int(row[1])}')
    row = next(c.execute(f'select sum(max(na, ni)) from midpoints_wt {w}'))
    print(f'Total lower bound: {int(row[0])}')

