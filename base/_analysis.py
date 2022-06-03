#!/usr/bin/env python3
#
# Shared analysis
#
import numpy as np
import scipy.stats


def gaussian(x, mu, sigma):
    """
    Return a gaussian/normal pdf over x, with mean mu and stddev sigma.
    """
    return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(
        -np.power((x - mu) / sigma, 2) * 0.5)


def individual_pdfs(rows):
    """
    Gathers data from the provided ``rows``, calculates a PDF for each entry
    with n>0, and returns a list of tuples with information.

    Arguments:

    ``rows``
        Each row in ``rows`` must contain five columns in the order
        ``(name, v, sem, n, std)``.

    Returns a list of tuples, where each row contains:

    ``pub``
        The name of the publication
    ``n``
        The total number of cells.
    ``x``
        X-coordinates for a gaussian distribution.
    ``y``
        Y-coordinates for a weighted gaussian distribution.
    ``mu``
        The mean.
    ``sigma``
        The standard deviation.

    """
    # Create x-data and y-data
    x = np.linspace(-140, 20, 1000)
    y = np.zeros(x.shape)

    # Gather data from rows
    data = []
    for k, row in enumerate(rows):
        pub, v, sem, n, std = row

        # Skip rows without act/inact measurement
        if n == 0:
            continue

        # Check std calculation
        if np.abs(std - sem * np.sqrt(n)) > 1e-6:
            print(f'Warning: Error in STD for {pub}')
            print(f'  Listed    : {std}')
            print(f'  Calculated: {sem * np.sqrt(n)}')

        # Calculate and store weighted PDF
        y = n * gaussian(x, v, std)
        data.append((pub, int(n), x, y, v, std))

    return data


def combined_pdf(rows):
    """
    Gathers data from the provided ``rows``, calculates a combined PDF, and
    returns a tuple of information.

    Arguments:

    ``rows``
        Each row in ``rows`` must contain five columns in the order
        ``(name, v, sem, n, std)``.

    Returns a tuple:

    ``data``
        A tuple ``(x, sum, gauss)`` containing x coordinates, a summed and
        weighted PDF, and a Gaussian approximation.
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
    for field in fields:
        v, std, n = data[field]

        # Create pdf, weighted by n / ntotal
        pdf = (n / ntotal) * gaussian(x, v, std)

        # Update sum
        y += pdf
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

    # Two-sigma range
    lo = mu - 2 * sigma
    hi = mu + 2 * sigma

    # Return
    return ([x, y, z], nmeasurements, int(ntotal), mu, sigma, lo, hi, p)
