# The lowess Package
This package provides a function to perform a LOWESS on [Pandas Series objects](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html "Pandas Series"). 
LOWESS (locally weighted scatterplot smoothing) \[1, 2\] as defined by STATA \[3\].
The regressions utilises some of the methods in \[4\].



## Description



### Methods and Formula
Let x and y be the two variables each of length N, and assume that the data are ordered so that x<sub>i</sub> ≤ x<sub>i+1</sub> for i = 1,...,N-1.
For each y<sub>i</sub>, a smoothed value y<sub>i</sub><sup>s</sup> is calculated.
The subset of points used in calculating y<sub>i</sub><sup>s</sup> is  i<sub>-</sub> = max(1, i-k) through i<sub>+</sub> = min(i+k, N), where  

k = Floor((N × bandwidth - 0.5) / 2).  

The weights for each of the observations between j = i<sub>-</sub>,...,i<sub>+</sub> are the tricube  

w<sub>j</sub> = [1 - (|x<sub>j</sub> - x<sub>i</sub>| / ∆)<sup>3</sup>]<sup>3</sup>,  

where ∆ = 1.0001 max(x<sub>i<sub>+</sub></sub>-x<sub>i</sub>, x<sub>i</sub>-x<sub>i<sub>-</sub></sub>).
The smoothed value y<sub>i</sub><sup>s</sup> is then the weighted polynomial regression prediction at x<sub>i</sub>.

**NB**: In this implemtation x and y should be Pandas Series objects.
The series need not be sorted and x and y can be in different orders, so long as their indexes have the same elements. 



### Usage
Once the package has been installed it can be imported into a python script  
`import lowess`  
The package provides a single module `lowess` with a single function `lowess.lowess`.
This function has the signiture:  
`lowess.lowess(x, y, bandwidth=0.2, polynomialDegree=1)`  
where the arguments are:
1. **x** (pandas.core.series.Series): a Pandas Series containing the x (independent/covariat) values. The indices must be unique.
2. **y** (pandas.core.series.Series): a Pandas Series containing the y (dependent) values. It must have the same index as x (although not necessarily in the same order.)
3. **bandwidth** (float, optional): the bandwidth for smoothing. It must be between 0 and 1. Default is 0.2
4. **polynomialDegree** (int, optional): The degree of polynomial to use in the regression. It must be >= 0. Default is 1.

It returns a Pandas Series containing the smoothed y values, with the same index as y.

If the input is not valid or an error occurs, a `LowessError` exception is raised.



## Examples
Some examples are given in the directory `examples`.



## Installation
### Via the PyPI package manager
The package can be installed with `pip` via the command:  
`$ pip install lowess`  

### Via GitHub
The package can be installed from source via GitHub.
First download the repository, either via SSH  

    $ git clone git@github.com:CCGE-Cambridge/lowess.git

or via HTTPS  

    $ git clone https://github.com/CCGE-Cambridge/lowess.git  
 
Then install the package via

    $ cd lowess
    $ pip install .

### Uninstall 
To uninstall use the command

    $ pip uninstall lowess

### Requirements
This package is built on several Python packages, which are listed in `requirements.txt`. 
They can be installed using the command

    $ pip install -r requirements.txt



## Documentaion
Documentaion of the API is provided via Sphinx.
To make the documentaion

    $ cd docs
    $ make html
    $ open build/html/index.html

This may require installation of the package `sphinx`.



## Testing
Unit tests are implemented via `unittest` and are in the file `tests/test_lowess.py`.
To run the tests first download the source code and then run the command:  

    $ python -m unittest discover

Coverage can be tested using `coverage` using:

    $ coverage run -m unittest discover
    $ coverage report -m 

This may require installation of the package `coverage`.



## License
Copyright (c) 2020 Andrew Lee

This software is provided as is without any warranty whatsoever.
Permission to use, for non-commercial purposes is granted.
Permission to modify for personal or internal use is granted,
provided this copyright and disclaimer are included in all
copies of the software. All other rights are reserved.
In particular, redistribution of the code is not allowed.



## References
1. Cleveland, W. S. 1979. Robust locally weighted regression and smoothing scatterplots. *Journal of the American Statistical Association* **74**: 829–836. [https://www.jstor.org/stable/2286407]
2. Wikipedia: Local Regression - [https://en.wikipedia.org/wiki/Local_regression] (accessed 2020-04-20)
3. STATA: Lowess - [https://www.stata.com/manuals13/rlowess.pdf] (accessed 2020-04-20)
4. Cappellari et al. 2013 The ATLAS<sup>3D</sup> project - XX. Mass-size and mass-&sigma; distributions of early-type galaxies: bulge fraction drives kinematics, mass-to-light ratio, molecular gas fraction and stellar initial mass function *Monthly Notices of the Royal Astronomical Society* **432**: 1862-1893 [https://doi.org/10.1093/mnras/stt644]
