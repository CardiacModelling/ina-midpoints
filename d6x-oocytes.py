#!/usr/bin/env python3
#
# Figure 2: Correlation between Va and Vi
#
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import base

# Gather data
print('Gathering data')
with base.connect() as con:
    c = con.cursor()

    # Get all data, plus data split into biggest subset and rest
    q = ('select pub, va, vi from midpoints_wt'
         ' where (na > 0 AND ni > 0 AND cell == "Oocyte")'
         ' order by va')
    for r in c.execute(q):
        print(r[0], r[1])

