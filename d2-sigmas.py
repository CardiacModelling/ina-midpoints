#!/usr/bin/env python3
#
# Calculates statistics about the standard deviations reported in the midpoints
# data.
#
import numpy as np

import base


q = 'select pub, na, ni, stda, stdi, sema, semi from midpoints_wt'

# Query db
na, ni = [], []
stda, stdi = [], []
sema, semi = [], []
with base.connect() as con:
    c = con.cursor()
    for row in c.execute(q):
        if row['na'] > 0:
            na.append(row['na'])
            stda.append(row['stda'])
            sema.append(row['sema'])
        if row['ni'] > 0:
            ni.append(row['ni'])
            stdi.append(row['stdi'])
            semi.append(row['semi'])

# Calculate
s90 = 1.6448536269514729
stdi = np.array(stdi)
stda = np.array(stda)
print('Standard deviation of inactivation')
print(f'Min:    {np.min(stdi)}')
print(f'Max:    {np.max(stdi)}')
print(f'Median: {np.median(stdi)}')
print('90th percentile activation')
print(f'Median: {np.median(stdi) * 2 * s90}')
print(f'Max:    {np.max(stdi) * 2 * s90}')
print()
print('Standard deviation of activation')
print(f'Min:    {np.min(stda)}')
print(f'Max:    {np.max(stda)}')
print(f'Median: {np.median(stda)}')
print('90th percentile activation')
print(f'Median: {np.median(stda) * 2 * s90}')
print(f'Max:    {np.max(stda) * 2 * s90}')
