Getting started
===============

Installation
--------------

Installation steps:

1. Download the project folder from https://github.com/owenwr/labour-flow-networks
2. Download the raw data folder. The data is private, contact Omar Guerrero; contact
   details are avaliable on his website, http://oguerr.com/.
3. Copy and paste the raw data folder into /data/raw/16-12-2016-Mega.
4. Check that all software requirements are satisfied.

Requirements
*************

All code is Python 2.7; all Python package requirements are in requirements.txt.
If you have pip, use command pip install -r requirements.txt from the command
line while in the labour-flow-networks project root directory and most recent
versions of all relevant packages will be installed automatically. If you don't
have pip installed then google Anaconda Python and download the relevant
Anaconda distribution for your operating system. This will give you pip.

Data
------

All data used in this project is stored in the /data folder. The rawest form of
the data I ever saw is in the /data/raw folder. However, this 'raw' data is
actually already processed, Omar Guerrero took it from the servers at Statistics
Finland and cleaned it. Some of the outputs of my analysis scripts save data in
the /data/processed folder.

Despite Omar's cleaning, there are problems with the data. For example, if you
look at the number of firms that died in each year it looks like the data is not
reliable before 1995. For this reason I tended to only analyse data from 1995
onwards. Patrick Dendorfer has also found anomalies/problems in the data.

LFN Class Objects
-------------------

In src/data/make_dataset_classes.py there is a class definition for an LFN
object. Familiarity with the LFN object is important since it is the basis
for everything. The class allows you to easily create and manipulate Labour
Flow Networks.

LFN Scripts
-------------

The src folder contains a number of scripts. These scripts are for pieces of
analysis I have done on Labour Flow Networks. Probably the most important is
shortest_path_lengths.py. This script analyses the shortest path lengths
between pairs of firms in general and between pairs of firms that died. The
idea is to see if firms that die tend to be closer to each other in the network
than random (a Monte Carlo simulation is used to find how far away we would
expect them to be at random).

Reports
--------

All the figures produced in scripts are saved in /reports/figures.

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