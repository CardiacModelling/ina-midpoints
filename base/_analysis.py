#!/usr/bin/env python3
#
# Provides a connection to the mutation database.
#
import numpy as np
import scipy.stats


def gaussian(x, mu, sigma):
    """
    Return a gaussian/normal pdf over x, with mean mu and stddev sigma.
    """
    return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(
        -np.power((x - mu) / sigma, 2) * 0.5)


def combined_pdf(rows, individual=False):
    """
    Gathers data from the provided ``rows``, calculates a combined PDF, and
    returns a tuple of information.

    Arguments:

    ``rows``
        Each row in ``rows`` must contain five columns in the order
        ``(name, v, sem, n, std)``.
    ``individual``
        If true, PDF info for each individual row will be returned (see below).

    Returns a tuple:

    ``data``
        A tuple ``(x, sum, gauss)`` containing x coordinates, a summed and
        weighted PDF, and a Gaussian approximation.
        If ``individual`` is set to ``True`` these will be followed by a PDF
        for each of the individual rows.
    ``m``
        The number of reports.
    ``n``
        The total number of cells.
    ``mean``
        The mean of the PDF.
    ``sigma``
        The standard deviation of the PDF.
    ``lo``
        The lower bound of the 2-sigma range.
    ``hi``
        The upper bound of the 2-sigma range.
    ``p``
        The p-value from a chi-squared test testing if the PDF is normal.

    """
    # High number of x-axis points, for accurate calculations
    npoints = 100000

    # Lower number of points, for fast representations
    xf = int(npoints // 1000)

    # Create x-data and y-data
    x = np.linspace(-140, 20, npoints)
    y = np.zeros(x.shape)

    # Names of each measurement
    fields = []
    # Result for each measurement (v, std, n)
    data = {}
    # Total number of cells measured
    ntotal = 0

    # Gather data from rows
    for k, row in enumerate(rows):
        pub, v, sem, n, std = row
        field = str(k) + '-' + pub
        # Skip rows without act/inact measurement
        if n == 0:
            continue
        # Check std calculation
        if np.abs(std - sem * np.sqrt(n)) > 1e-6:
            print(f'Warning: Error in STD for {field}')
            print(f'  Listed    : {std}')
            print(f'  Calculated: {sem * np.sqrt(n)}')
        # Update ntotal
        ntotal += n
        # Store data
        fields.append(field)
        data[field] = (v, std, n)

    # Create probability density functions
    nmeasurements = len(fields)
    pdfs = {}
    for field in fields:
        v, std, n = data[field]

        # Create pdf, weighted by n / ntotal
        pdf = (n / ntotal) * gaussian(x, v, std)

        # Update sum
        y += pdf

        # Store reduced data
        if individual:
            pdfs[field] = pdf[::xf]
    del(data)

    # Calculate mean and standard deviation
    mu = np.sum(x * y) / np.sum(y)
    sigma = np.sqrt(np.sum(y * ((x - mu) ** 2)) / np.sum(y))

    # Test goodness of fit using a chi-squared test
    z = gaussian(x, mu, sigma)
    chisq, p = scipy.stats.chisquare(
        y / np.sum(y),
        z / np.sum(z),
        2,  # 2 params used to estimate z
    )

    # Area under PDF
    # print(f'Area under PDF: {np.sum(y) * (x[1] - x[0])}')

    # Reduce data
    x = x[::xf]
    y = y[::xf]

    # Draw gaussian curve
    z = gaussian(x, mu, sigma)

    # Create output
    data = [x, y, z]
    if individual:
        data += [pdfs[f] for f in fields]

    # Two-sigma range
    lo = mu - 2 * sigma
    hi = mu + 2 * sigma

    # Return
    return (data, nmeasurements, int(ntotal), mu, sigma, lo, hi, p)
