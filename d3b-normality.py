#!/usr/bin/env python3
import numpy as np

s90 = 1.6448536269514729

n = 1000000
x = np.random.uniform(0, 100, size=n)
print(f'Real 90th percentile range: 90')
print(f'Estimated                 :', np.std(x) * 2 * s90)
