#!/usr/bin/env python3
#
# Calculates statistics about the means reported in the midpoints data.
#
import numpy as np

import base

q = 'select vi, ni, va, na from midpoints_wt'

# Query db
na, ni = [], []
va, vi = [], []
with base.connect() as con:
    c = con.cursor()
    for row in c.execute(q):
        if row['na'] > 0:
            va.append(row['va'])
        if row['ni'] > 0:
            vi.append(row['vi'])

# Calculate
va = np.array(va)
vi = np.array(vi)
print('Mean midpoint of activation')
print(f'Min:   {np.min(va)}')
print(f'Max:   {np.max(va)}')
print(f'Mean:  {np.mean(va)}')
print(f'Range: {np.max(va) - np.min(va)}')
print('Mean midpoint of inactivation')
print(f'Min:   {np.min(vi)}')
print(f'Max:   {np.max(vi)}')
print(f'Mean:  {np.mean(vi)}')
print(f'Range: {np.max(vi) - np.min(vi)}')
