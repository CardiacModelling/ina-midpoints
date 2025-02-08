#!/usr/bin/env python3
#
# Calculates statistics about the means reported in the midpoints data.
#
import numpy as np

import base

nooocytes = True
qand = ' and cell != "Oocyte"'

# Query db
with base.connect() as con:
    c = con.cursor()
    q = f'select ki from midpoints_wt where ki is not null {qand}'
    ki = np.array([row['ki'] for row in c.execute(q)])
    q = f'select ka from midpoints_wt where ka is not null {qand}'
    ka = np.array([row['ka'] for row in c.execute(q)])

# Calculate
print('Slope of inactivation')
print(f'Min:    {np.min(ki)}')
print(f'Max:    {np.max(ki)}')
print(f'Median: {np.median(ki):.1f}')
print(f'Range:  {np.max(ki) - np.min(ki):.1f}')
print(f'90th p: {np.percentile(ki, 95) - np.percentile(ki, 5):.1f}')
print()
print('Slope of activation')
print(f'Min:    {np.min(ka)}')
print(f'Max:    {np.max(ka)}')
print(f'Median: {np.median(ka):.1f}')
print(f'Range:  {np.max(ka) - np.min(ka):.1f}')
print(f'90th p: {np.percentile(ka, 95) - np.percentile(ka, 5):.1f}')

