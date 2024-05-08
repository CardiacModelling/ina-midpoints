#!/usr/bin/env python3
#
# Retrieves the number of publications per journal
#
import base

nooocytes = True

w = 'where cell != "Oocyte"' if nooocytes else ''


with base.connect() as con:
    c = con.cursor()
    q = ('select journal, COUNT(pub) from midpoints_wt inner join publication'
         f' on midpoints_wt.pub = publication.key {w}'
         ' group by publication.journal order by publication.journal')
    for row in c.execute(q):
        print(list(row))

    # Sanity check
    print(sum([row[1] for row in c.execute(q)]))
