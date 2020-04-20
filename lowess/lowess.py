'''
:author: Andrew Lee
:organization: CCGE, PHPC, The University of Cambridge
:license: GNU General Public License, version 3
:contact: ajl65@cam.ac.uk
'''
import numpy as np
import pandas as pd


__version__ = 'v1.?.?'


class LowessError(Exception):
    '''
    LowessError raised for errors in lowess smoothing.

    Args:
        detail (str): Explanation of why the exception was raised.

    '''

    def __init__(self, detail):
        super().__init__({'LowessError': detail})


def lowess(x, y, bandwidth=0.2, polynomialDegree=1):
    '''
    Function to calculate the lowess smoothed estimate as per STATA
    https://www.stata.com/manuals13/rlowess.pdf
    It uses a tricibic weighting.

    Args:
        x (pandas.core.series.Series): a Pandas Series containing the x
            (independent/covariat) values.
        y (pandas.core.series.Series): a Pandas Series containing the y
            (dependent) values. It must have the same index as x, although
            not necessarily in the same order.
        bandwidth (float, optional): the bandwidth for smoothing. It must be
            between 0 and 1.
        polynomialDegree (int, optional): The degree of polynomial to use in
            the regression. It must be >= 0.

    Returns:
        pandas.core.series.Series: a Pandas Series containing the smoothed y
            values.

    Raises:
        LowessError: If input is not valid or an error occurs.

    '''

    # Validate the inputs
    validateInput(x, y, bandwidth, polynomialDegree)

    # Initialise a Pandas Series for the results.
    ySmooth = pd.Series(index=y.index, dtype=y.dtype)

    # Create maps from the index to the ordinal position (based on value)
    # and back.
    mapI2P, mapP2I = Index2PositionMap(x)

    # Loop through x values, and perfrom a regression for each.
    for index, value in x.items():
        # Determine the set of points to use in the regression.
        points, point = neighbours(mapP2I, mapI2P[index], bandwidth)
        # Determine the weights for the regression
        weights = triCubicWeights(x[points], value)
        # Perform the regression
        ySmooth[index] = wLstSqReg(x[points], y[points], 1, weights)[point]

    return ySmooth


def validateInput(x, y, bandwidth, polynomialDegree):
    '''
    Validate the input for the lowess smoothing.

    Args:
        x (pandas.core.series.Series): a Pandas Series containing the x
            (independent/covariat) values.
        y (pandas.core.series.Series): a Pandas Series containing the y
            (dependent) values. It must have the same index as x, although
            not necessarily in the same order.
        bandwidth (float): the bandwidth for smoothing (between 0 and 1)
        polynomialDegree (int): The degree of polynomial to use in the
            regression.

    Raises:
        LowessError: If input is not valid occurs.

    '''

    # Check x and y.
    for s in [x, y]:
        # Check that it is a Pandas Series.
        if not isinstance(s, pd.core.series.Series):
            raise LowessError('x or y is not a Pandas series.')

        # Check that it is numeric
        try:
            _ = s.astype(np.float64)
        except Exception:
            raise LowessError('x or y is not of numeric type.')

        # Check for Bools
        if any([isinstance(i, bool) for i in s]):
            raise LowessError('x or y contains a Bool.')

        # Check for null values
        if s.isna().values.any():
            raise LowessError('x or y contains null/na/NaN/None values.')

    # Check that x and y have the same indices.
    if len(y.index) != len(x.index):
        raise LowessError('x and y indices are not the same length.')
    if not all([i in [i for i in y.index] for i in [i for i in x.index]]):
        raise LowessError('x and y indices are not equivalent.')

    # Check that the value of the bandwidth is within range.
    if not isinstance(bandwidth, float):
        raise LowessError('bandwidth is not a float.')
    if not (0.0 < bandwidth < 1.0):
        raise LowessError('bandwidth is out or range.')

    # Check that the degree of the polynomial is valid
    if ((not isinstance(polynomialDegree, int)) or
       (isinstance(polynomialDegree, bool))):
        raise LowessError('polynomialDegree is not an integer.')
    if polynomialDegree < 0:
        raise LowessError('polynomialDegree is less than zero.')

    return


def Index2PositionMap(x):
    '''
    Create maps from the index to the ordinal position (based on value)
    and back.

    Args:
        x (pandas.core.series.Series): a Pandas Series

    Returns:
        (pandas.core.series.Series, pandas.core.series.Series):
            1) A Pandas Series with the same indices as x (although not
                necessarily in the same order) and with values corresponding
                to ordered positions.
            2) A Pandas Series containing the indices of x as values indixed
                by ordered positions.

    '''

    mapI2P = pd.Series(range(len(x)))
    mapI2P.index = x.index[x.argsort()]
    mapP2I = pd.Series(mapI2P.index.values, index=mapI2P)
    return mapI2P, mapP2I


def neighbours(mapP2I, pos, bandwidth):
    '''
    Determines the set of points within the bandwidth of position,
    and the index of the origianl position within that set.

    Args:
        mapP2I (pandas.core.series.Series): a map from position to index.
        pos (int): the position of the point of interest.
        bandwidth (float): the bandwidth of points to take.

    Returns:
        (pandas.core.series.Series, int):
            1) The set of points within the bandwidth.
            2) The index of the original point within the set.

    '''

    # Calculate the number of points corresponding to the bandwidth
    N = len(mapP2I)
    k = int(np.floor((N * bandwidth - 0.5) / 2.0))

    # Calculate the lower and upper limits
    lower = max(0, pos - k)
    upper = min(pos + k + 1, N)

    # Slice the array and get the index of the original point.
    return mapP2I[lower:upper], mapP2I[lower:upper].index.get_loc(pos)


def triCubicWeights(x, xi):
    '''
    Calculate the weights for the regression.

    Args:
        x (pandas.core.series.Series): a set of points.
        xi (float): The specific point in the set with respect to which the
            weights are calculated.

    Returns:
        pandas.core.series.Series: The set of regression weights to use at xi.

    '''

    diffs = abs(x - xi)
    return (1.0 - (diffs / (1.0001 * max(diffs))) ** 3) ** 3


def wLstSqReg(x, y, polynomialDegree, weights):
    '''
    Weighted least squares regression of a polynomial to the data (x, y)
    with weights.

    Args:
        x (pandas.core.series.Series): a Pandas Series containing the x
            (independent/covariat) values.
        y (pandas.core.series.Series): a Pandas Series containing the y
            (dependent) values. It must have the same index as x.
        polynomialDegree (int): The degree of polynomial to use in the
            regression. It must be >= 0.
        weights (pandas.core.series.Series): The set of regression weights to
            be used

    Returns:
        pandas.core.series.Series: The fitted function evaluated at each point
            in x.

    Raises:
        LowessError:
            1) There are more unknowns than data points in the
                regression.
            2) If an error occurs.

    '''

    # Check that the are at least as many data points as regression
    # coefficients (unknowns). This is not necessary, as linalg.lstsq should
    # still work (with an SVD cut), but it is not a good sign.
    if len(x) < polynomialDegree:
        raise LowessError('The least squares regreesion is under determined.'
                          'There are more fit variables than data points.')

    # Create a 2D array with the monomials for each power up to
    # polynomialDegree for each row in x
    monomials = (x.astype(np.float64)[:, np.newaxis] **
                 np.arange(polynomialDegree + 1))

    # Take the square root of the weights
    sigma = np.sqrt(weights.astype(np.float64))

    # Solve for the regression coefficients.
    try:
        beta = np.linalg.lstsq(monomials * sigma[:, np.newaxis],
                               y.astype(np.float64) * sigma,
                               rcond=None)[0]
    except Exception:
        raise LowessError('The least squares regression failed.')

    # Return the fitted function evaluated at each point
    return monomials.dot(beta)
