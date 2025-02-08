#!/usr/bin/env python3
#
# Measurement closest to the mean
#
import base
import numpy as np


pub, va, vi = [], [], []
with base.connect() as con:
    c = con.cursor()
    q = ('select pub, va, vi from midpoints_wt'
         f' where (na > 0 and ni > 0 and cell != "Oocyte")')
    for row in c.execute(q):
        pub.append(row[0])
        va.append(float(row[1]))
        vi.append(float(row[2]))

va, vi = np.array(va), np.array(vi)
ma, mi = np.mean(va), np.mean(vi)

print(ma, mi)

distance = np.sqrt((va - ma)**2 + (vi - mi)**2)
order = np.argsort(distance)

for i in order:
    print(pub[i], distance[i])
