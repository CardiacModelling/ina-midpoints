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
stda = np.array(stda)
stdi = np.array(stdi)
print('Standard deviation of activation')
print(f'Min:  {np.min(stda)}')
print(f'Max:  {np.max(stda)}')
print(f'Mean: {np.mean(stda)}')
print('Standard deviation of inactivation')
print(f'Min:  {np.min(stdi)}')
print(f'Max:  {np.max(stdi)}')
print(f'Mean: {np.mean(stdi)}')

