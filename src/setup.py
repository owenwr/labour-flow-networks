'''
Setup script for compiling Cython code.

I usually use pyxinstall to automate the compiling process rather than running
this script. Mainly because there seems to be a bug with Mac Python that means
it all gets confused with the numpy import.
'''

from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

def main():
    setup(
        name = "C_shortest_path_lengths",
        ext_modules = cythonize(
                        'C_shortest_path_lengths.pyx',
                        include_path = [np.get_include()]
            ),  # accepts a glob pattern
    )

if __name__ == '__main__':
    main()
