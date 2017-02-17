Getting started
===============

This is where you describe how to get set up on a clean install, including the
commands necessary to get the raw data (using the `sync_data_from_s3` command,
for example), and then how to make the cleaned, final data sets.

src/data/make_dataset.py
========================

Includes functions for getting started. The function MakeLFN will generate a
Labour Flow Network from the data with minimal effort - just put in the dates
you want to get flows from in a string of the form 'year1-year2' as the
argument of the function and it will spit out an LFN.

src/shortest_path_lengths.py
============================

Script for analyzing the lengths of the shortest paths between nodes that have
died in the Labour Flow Network.

Filename Conventions
=====================

'flowyearsxxxx-yyyy': signifies that the LFN in use was constructed from all
the flows after year xxxx and before year yyyy.

'deathsxxxx-yyyy': signifies that firm deaths considered are those that
occurred after year xxxx and before year yyyy.

'res': signifies results generated from the actual deaths of firms (as 
opposed to results from randomly generated deaths in a test or Monte 
Carlo simulation).

'mc_res': results generated from randomly generated Monte Carlo runs.