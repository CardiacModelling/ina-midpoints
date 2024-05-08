#!/usr/bin/env python3
#
# 5 to 95th-percentile of a normal distribution, used to calculate
#
import scipy

# Get the 5-th percentile point of a normal distribution, centered at 0
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
p05 = scipy.stats.norm.ppf(0.05)

# If we integrate up to this value, we expect to find 5% of the total area
print('Should be 5%:', scipy.stats.norm.cdf(p05))

# So 90% of the values are within -p05 and +p05
print('Should be 90%:', scipy.stats.norm.cdf(-p05) - scipy.stats.norm.cdf(p05))

# The width of this bracket is 2 * -p05
print('Width of the 5th-95th percentile range:', 2 * -p05)
print('Alternatively, +-', -p05)

