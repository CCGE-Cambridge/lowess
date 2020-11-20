'''
Test suite for lowess package
'''
import sys
import logging
import unittest
import pandas as pd
import numpy as np
import lowess
from lowess import LowessError

logger = logging.getLogger(__name__)


class TestLowess(unittest.TestCase):
    def setUp(self):
        # Load the test data.
        self.knownResults = pd.read_csv('tests/testData/test_data_STATA.csv',
                                        index_col='index')
        pass

    def tearDown(self):
        del self.knownResults
        pass

    def testValidData(self):
        '''
        Call lowess with valid data, and check that an exception is not raised.
        '''
        try:
            _ = lowess.lowess(self.knownResults['x'],
                              self.knownResults['y'],
                              bandwidth=0.2,
                              polynomialDegree=1)
        except Exception:
            logger.warning("Unexpected error:", sys.exc_info()[0])
            raised = True
        else:
            raised = False
        self.assertFalse(raised, 'Exception not raised')

    def testInvalidX(self):
        '''
        Try calling the function with an invalid x, and check that an
        exception is raised.
        '''
        xNaN = self.knownResults['x'].copy()
        xNaN[5] = np.NaN
        xNonNumeric = self.knownResults['x'].copy()
        xNonNumeric[5] = 'invalid'
        xBool = self.knownResults['x'].copy()
        xBool[5] = True
        xLong = self.knownResults['x'].copy().append(pd.Series([0.1],
                                                     index=['a']))
        xIndex = self.knownResults['x'].copy()
        xIndex.index = [i + 100 for i in range(len(xIndex))]
        invalids = [self.knownResults['x'].to_numpy(), 'a', True, xNaN,
                    xNonNumeric, xBool, xLong, xIndex]
        for x in invalids:
            with self.assertRaises(LowessError):
                _ = lowess.lowess(x,
                                  self.knownResults['y'],
                                  bandwidth=0.2,
                                  polynomialDegree=1)

    def testDuplicateIndex(self):
        '''
        Try calling the function with a ducplicated index, and check that an
        exception is raised.
        '''
        df = self.knownResults.rename({self.knownResults.index[1]:
                                       self.knownResults.index[0]})
        with self.assertRaises(LowessError):
            _ = lowess.lowess(df['x'],
                              df['y'],
                              bandwidth=0.2,
                              polynomialDegree=1)

    def testInvalidY(self):
        '''
        Try calling the function with an invalid y, and check that an
        exception is raised.
        '''
        yNaN = self.knownResults['y'].copy()
        yNaN[5] = np.NaN
        yNonNumeric = self.knownResults['y'].copy()
        yNonNumeric[5] = 'invalid'
        yBool = self.knownResults['y'].copy()
        yBool[5] = 'True'
        yLong = self.knownResults['y'].copy().append(pd.Series([0.1],
                                                     index=['a']))
        invalids = [self.knownResults['y'].to_numpy(), 'a', True, yNaN,
                    yNonNumeric, yBool, yLong]
        for y in invalids:
            with self.assertRaises(LowessError):
                _ = lowess.lowess(self.knownResults['x'],
                                  y,
                                  bandwidth=0.2,
                                  polynomialDegree=1)

    def testInvalidBandwidth(self):
        '''
        Try calling the function with an invalid bandwidth, and check that an
        exception is raised.
        '''
        invalids = [-0.1, 1.2, '0.7', True, [0.1], None, 1, 0]
        for bw in invalids:
            with self.assertRaises(LowessError):
                _ = lowess.lowess(self.knownResults['x'],
                                  self.knownResults['y'],
                                  bandwidth=bw,
                                  polynomialDegree=1)

    def testInvalidPolynomialDegree(self):
        '''
        Try calling the function with an invalid polynomialDegree, and check
        that an exception is raised.
        '''
        invalids = [-1, 1.2, '1', True, [1], None, len(self.knownResults) + 1]
        for dg in invalids:
            with self.assertRaises(LowessError):
                _ = lowess.lowess(self.knownResults['x'],
                                  self.knownResults['y'],
                                  bandwidth=0.2,
                                  polynomialDegree=dg)

    def testKnownResults(self):
        '''
        Test the function against known STATA results
        '''
        correct = []
        for deg in [0, 1]:
            for i in range(1, 10):
                bwidth = 0.1 * i
                tmp = lowess.lowess(self.knownResults['x'],
                                    self.knownResults['y'],
                                    bandwidth=bwidth,
                                    polynomialDegree=deg)
                col = 'y_Stata_{}_{}'.format(i, deg)
                self.knownResults
                correct.append(max(abs((self.knownResults[col] - tmp) /
                                       (self.knownResults[col] + tmp))) < 1e-5)
        self.assertTrue(all(correct), 'Results the same as STATA.')

    def testOrder(self):
        '''
        Shuffle the rows and check that the result is unchanged.
        '''
        result = lowess.lowess(self.knownResults['x'],
                               self.knownResults['y'],
                               bandwidth=0.5,
                               polynomialDegree=1)
        result2 = lowess.lowess(self.knownResults['x'].sample(frac=1),
                                self.knownResults['y'].sample(frac=1),
                                bandwidth=0.5,
                                polynomialDegree=1)

        eql = all([abs((result[i] - result2[i]) / (result[i] + result2[i])) <
                  1e-10 for i in result.index])
        self.assertTrue(eql, 'Results equal on shuffle.')


if __name__ == '__main__':
    unittest.main()
