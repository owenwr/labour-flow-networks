setup module
================

Includes a Cython import so I got rid of the automodule.

Setup script for manually compiling Cython code.

I usually use pyxinstall to automate the compiling process rather than running
this script. Mainly because there seems to be a bug with Mac Python that means
it all gets confused with the numpy import.