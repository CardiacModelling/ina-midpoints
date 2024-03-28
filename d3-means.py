#!/usr/bin/env python3
#
# Calculates statistics about the means reported in the midpoints data.
#
import numpy as np

import base

nooocytes = True

q = 'select vi, ni, va, na from midpoints_wt'
if nooocytes:
    q += ' where cell != "Oocyte"'

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
vi = np.array(vi)
va = np.array(va)
print('Mean midpoint of inactivation')
print(f'Min:    {np.min(vi)}')
print(f'Max:    {np.max(vi)}')
print(f'Median: {np.median(vi):.1f}')
print(f'Range:  {np.max(vi) - np.min(vi):.1f}')
print()
print('Mean midpoint of activation')
print(f'Min:    {np.min(va)}')
print(f'Max:    {np.max(va)}')
print(f'Median: {np.median(va):.1f}')
print(f'Range:  {np.max(va) - np.min(va):.1f}')

