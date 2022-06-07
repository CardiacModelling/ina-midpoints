#!/usr/bin/env python3
#
# Calculates max between exp var in Kapplinger and Tan
#
import base


with base.connect() as con:
    c = con.cursor()

    pub = 'Kapplinger 2015'
    print(pub)
    r = next(c.execute('select min(Va), max(Va) from midpoints_wt where pub is'
                       f' "{pub}";'))
    print(f'  Va: {r[0]}, {r[1]} ({r[1] - r[0]})')
    r = next(c.execute('select min(Vi), max(Vi) from midpoints_wt where pub is'
                       f' "{pub}";'))
    print(f'  Vi: {r[0]}, {r[1]} ({r[1] - r[0]})')

    pub = 'Tan 2005'
    print(pub)
    r = next(c.execute('select min(Va), max(Va) from midpoints_wt where pub is'
                       f' "{pub}";'))
    print(f'  Va: {r[0]}, {r[1]} ({r[1] - r[0]})')
    r = next(c.execute('select min(Vi), max(Vi) from midpoints_wt where pub is'
                       f' "{pub}";'))
    print(f'  Vi: {r[0]}, {r[1]} ({r[1] - r[0]})')
