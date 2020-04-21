#!/usr/bin/env python3
import pandas as pd
import numpy as np
import lowess
import sys
from itertools import cycle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot(df, xvar, fname):
    '''
    Function to plot the raw and smoothed data
    '''

    # Set the colours for the lines/points
    cm = plt.get_cmap('gist_ncar')
    nColours = len(df.columns) - 1
    colors = cycle([cm(1.0 * i / nColours) for i in range(nColours)])

    # Plot a line for each column in the DataFrame
    for column in df.columns:
        if column == xvar:
            pass
        elif column.lower() == 'raw':
            # Plot the unsmoothed data as scatter points
            plt.scatter(df[xvar], df[column], label=column, alpha=0.7,
                        color=next(colors))
        else:
            # Plot the smoothed data as a line
            plt.plot(df[xvar], df[column], label=column, linewidth=2.0,
                     alpha=0.5, color=next(colors))

    # Set the axis labels
    plt.xlabel('x', fontsize=14)
    plt.ylabel('y', fontsize=14)

    # Set the legend, axis limits, grid and ticks
    plt.legend(loc=2, frameon=False, prop={'size': 12})
    plt.grid(True)
    plt.tick_params(axis='both', which='major', labelsize=13)

    # Save the plot to a file, and close
    plt.savefig(fname,
                format='png',
                dpi=100,
                bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    '''
    Smooth a noisy quadratic signal using LOWESS varing the degree of the
    polynomial used in the regression.

    The 0th and 1st order polynomials will miss the large scal curvature.
    The higher order polynomials will over fit (high frequency oscillations.)
    '''

    # Generate some noisy data
    x = np.arange(-10, 10, 0.1)
    y = 1.0 + 2.0 * x + 0.3 * x ** 2 + 20.0 * np.random.random(len(x))

    # Create a Pandas DataFrame with the data
    df = pd.DataFrame({'x': x, 'Raw': y})

    # Smooth the data
    for i in range(5):
        label = 'polynomialDegree={}'.format(i)
        df[label] = lowess.lowess(df['x'], df['Raw'], bandwidth=0.3,
                                  polynomialDegree=i)

    # Plot the data
    plot(df, 'x', sys.argv[0].replace('.py', '.png'))
