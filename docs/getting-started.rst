Getting started
===============

All code is Python 2.7; all Python package requirements are in requirements.txt.
If you have pip, use command pip install -r requirements.txt from the command
line while in the labour-flow-networks project root directory and most recent
versions of all relevant packages will be installed automatically. If you don't
have pip installed then google Anaconda Python and download the relevant
Anaconda distribution for your operating system. This will give you pip.

Filename Conventions
---------------------

'flowyearsxxxx-yyyy': signifies that the LFN in use was constructed from all
the flows after year xxxx and before year yyyy.

'deathsxxxx-yyyy': signifies that firm deaths considered are those that
occurred after year xxxx and before year yyyy.

'res': signifies results generated from the actual deaths of firms (as 
opposed to results from randomly generated deaths in a test or Monte 
Carlo simulation).

'mc_res': results generated from randomly generated Monte Carlo runs.