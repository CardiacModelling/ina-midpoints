#!/usr/bin/env python3
#
# Calculates statistics about the standard deviations reported in the midpoints
# data.
#
import numpy as np

import base

nooocytes = True

q = 'select pub, na, ni, stda, stdi, sema, semi from midpoints_wt'
if nooocytes:
    q += ' where cell != "Oocyte"'

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
w90 = 3.2897072539029457
stdi = np.array(stdi)
stda = np.array(stda)
print('Standard deviation of inactivation')
print(f'Min:    {np.min(stdi)} ({np.min(stdi):.1f})')
print(f'Max:    {np.max(stdi)} ({np.max(stdi):.1f})')
print(f'Median: {np.median(stdi)} ({np.median(stdi):.1f})')
print('90th percentile activation')
print(f'Median: {np.median(stdi) * w90} ({np.median(stdi) * w90:.0f})')
print(f'Max:    {np.max(stdi) * w90} ({np.max(stdi) * w90:.0f})')
print()
print('Standard deviation of activation')
print(f'Min:    {np.min(stda)} ({np.min(stda):.1f})')
print(f'Max:    {np.max(stda)} ({np.max(stda):.1f})')
print(f'Median: {np.median(stda)} ({np.median(stda):.1f})')
print('90th percentile activation')
print(f'Median: {np.median(stda) * w90} ({np.median(stda) * w90:.0f})')
print(f'Max:    {np.max(stda) * w90} ({np.max(stda) * w90:.0f})')
