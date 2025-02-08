#!/usr/bin/env python3
#
# Calculates statistics about the means reported in the midpoints data.
#
import numpy as np

import base

nooocytes = True
qand = ' and cell != "Oocyte"' if nooocytes else ''

# Query db
na, ni = [], []
va, vi = [], []
with base.connect() as con:
    c = con.cursor()
    q = f'select vi from midpoints_wt where ni > 0 {qand}'
    vi = np.array([row['vi'] for row in c.execute(q)])
    q = f'select va from midpoints_wt where na > 0 {qand}'
    va = np.array([row['va'] for row in c.execute(q)])

# Calculate
print('Mean midpoint of inactivation')
print(f'Min:    {np.min(vi)}')
print(f'Max:    {np.max(vi)}')
print(f'Median: {np.median(vi):.1f}')
print(f'Range:  {np.max(vi) - np.min(vi):.1f}')
print(f'90th p: {np.percentile(vi, 95) - np.percentile(vi, 5):.1f}')
print()
print('Mean midpoint of activation')
print(f'Min:    {np.min(va)}')
print(f'Max:    {np.max(va)}')
print(f'Median: {np.median(va):.1f}')
print(f'Range:  {np.max(va) - np.min(va):.1f}')
print(f'90th p: {np.percentile(va, 95) - np.percentile(va, 5):.1f}')

