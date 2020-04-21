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
    Function to plot the raw and smoothed data.
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
    Smooth a noisy sine signal using LOWESS varing the bandwidth used to select
    the set of local points for the regression.

    The smaller bandwidths will fit noise.
    The larger bandwidths will miss the oscillating signal.
    '''

    # seed the random number generator so results reproducible
    np.random.seed((1, 2, 3))

    # Generate some noisy data
    x = np.arange(-10, 5, 0.1)
    y = np.sin(x) - 0.5 + np.random.random(len(x))

    # Create a Pandas DataFrame with the data
    df = pd.DataFrame({'x': x, 'Raw': y})

    # Smooth the data
    for i in ['0.05', '0.1', '0.3', '0.5', '0.7']:
        label = 'bandwidth={}'.format(i)
        df[label] = lowess.lowess(df['x'], df['Raw'], bandwidth=float(i),
                                  polynomialDegree=1)

    # Plot the data
    plot(df, 'x', sys.argv[0].replace('.py', '.png'))
