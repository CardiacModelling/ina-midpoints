#!/usr/bin/env python3
#
# Pulls lowest and highest temperatures from the database.
#
import base


with base.connect() as con:
    c = con.cursor()

    # Get lowest and highest T reported
    row = next(c.execute('select min(tmin), max(tmax) from midpoints_wt'))
    print(f'Minimum T: {row[0]}')
    print(f'Maximum T: {row[1]}')

    # Get smallest, biggest, mean delta-T reported
    q = ('select min(tmax-tmin), max(tmax-tmin), avg(tmax-tmin)'
         ' from midpoints_wt')
    row = next(c.execute(q))
    print(f'Minimum dT: {row[0]}')
    print(f'Maximum dT: {row[1]}')
    print(f'Average dT: {row[2]}')

