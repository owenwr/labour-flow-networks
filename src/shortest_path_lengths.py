'''
Introduction
*************

Script to get shortest path lengths (what I call ell values) between pairs
of dead nodes in a Labour Flow Network. The ell value is calculated for every
pair of dead nodes; the calculation is then repeated many times with randomly
selected 'dead' nodes.

Motivation
************

We want to determine whether there is a pattern to how firms die in a Labour
Flow Network. Specifically, this script tests for a pattern in the network
distances between firms that die. It does so by finding the number of pairs of
dead firms with each ell value. A Monte Carlo Simulation is used to put the
results into context. In the simulation, a set number of firms are chosen to
'die' at random, and the number of firms with each ell value is found. Once
the results are plotted using the make_shortest_path_lengths_figures we can
compare, eg, the number of pairs of dead firms with ell value 2 (ie, the
shortest path between them in the network has length 2) with the number of pairs
of firms with ell value 2 in each of the Monte Carlo Simulations.

Details
*********

**ell value** : The ell value for a pair of nodes in a Labour Flow Network is
the length of the shortest path between them. The path can pass through alive
and dead nodes (ie, we are not restricted to only travel through living nodes
when finding the shortest path).

1. Create LFN based on the flows in some chosen time period.
2. Determine dead firms based on firm deaths in some other chosen time period.
3. Find the length of the shortest path between each pair of nodes in the LFN (
   ie, find all the ell values).
4. Find the subset of the list of ell values that correspond to the shortest
   path lengths between each pair of *dead* firms.
5. Repeat step 4 but with the dead firms being chosen at random. The total
   number of dead firms is not random (it is chosen to be the same as in 4), but
   the nodes that die are randomly selected.

The docstring for the main() function includes information on the parameters.
See the docstring for full details, but note in partcicular
- The *nflowrows* parameter : if chosen to be a small number, small LFNs can be
generated to be used in quickly testing the code for obvious bugs.
- The *nrand* parameter : allows control over the number of firms that are
chosen randomly. See the the docstring of DeadRowsPartialRand below and the docs
for script chooseE.py for full details. In short, this parameter allows
the 'dead' nodes in the Monte Carlo Simulation to be chosen partially at random
and partially through a specified algorithm. This was an attempt to create Monte
Carlo results that looked more like the actual results. If we could get some
Monte Caro algorithm to look like the real results then that suggests we might
have a model for what's really happening.

The docstring also explains the format of the output. In short, the output
for a run with a given set of parameters is two pickled python dictionaries.
Both are of the form dict[ell] = number of pairs of nodes with that ell
value. In the res dictionary, we have dict[ell] = number of pairs of actually
dead nodes with this ell value, in the mcres dictinoary it is instead a list
of the number of 'dead' nodes with this ell value in each of the Monte Carlo
runs.

Notes
******

Ahsen Uppal at George Washington University suggested me that I could
speedup my current shortest_lengths.py Script by moving to numpy matrices. This
would be instead of using the Cython module.

Functions
************

'''

#================================================
#---imports and env variables-----
#================================================
import os
import numpy as np
import networkx as nx
import pandas as pd
import tqdm #package for monitoring the progress of for loops with a progresbar
import random
import pickle as pkl
import data.make_dataset_classes as dat
import general as gen #a miscellanious set of functions

import Cython
import pyximport
pyximport.install(setup_args={ "include_dirs":np.get_include()})
import C_shortest_path_lengths as Cshp

project_root = os.path.join(os.path.dirname(__file__), os.pardir)

#================================================
#---define functions-----
#================================================

def SHPToArray(shp_dictofdicts):
    '''
    Transform dict of dicts to array plus dictionay mapping firm IDs to row
    numbers and tuple mapping row numbers to firm IDs.

    Args:
        - shp_dictofdicts : dict
            Dictionary of dictionaries such that d[i][j] is the shortest path
            length between firms i and j.

    Returns:
        - shp_array: array
            Array such that a[i][j] is the shortest path length between firms i
            and j.
        - row_to_id : tuple
            Tuple such that row_to_id[i] gives the firm ID that row i in
            shp_array corresponds to.
        - id_to_row: dict
            dictionary such that id_to_row[i] gives the row in shp_array that ID
            i maps to.

    '''
    shp_df = pd.DataFrame(shp_dictofdicts)
    shp_df = shp_df.fillna(-1) #fill NaNs (which correspond to no path) with -1
    print('Warning: changing dtype in this way might not be RAM efficient')
    shp_df = pd.DataFrame(shp_df, dtype=np.int) #change dtype from float to int
    shp_array = shp_df.as_matrix()
    row_to_id = tuple(shp_df.index)
    id_to_row = {}
    for i in range(len(row_to_id)):
        id_to_row[row_to_id[i]] = i
    return shp_array, row_to_id, id_to_row

def DeadRows(dead_ids, id_to_row):
    '''
    Take IDs of dead firms and return array of rows of shp_array that are dead

    --Note that firm ids for firms that are not in the LFN are discarded--
    '''
    dead_ids = set(dead_ids)
    ids_in_g = set(id_to_row.keys())
    #get ids that are both in g and are dead.
    dead_ids_in_g = dead_ids.intersection(ids_in_g)
    return np.array([id_to_row[x] for x in dead_ids_in_g])

def DeadRowsRand(number_dead, all_rows):
    '''
    Get a random selection of n=number_dead dead rows from the shortest paths
    array.

    Note that all_rows is a mutable type and is passed by value so this function
    changes it, that doesn't matter though - it's just shuffling the order.

    Args:
        - number_dead: number of rows we want to kill
        - all_rows: list of all the rows (which represent firms in the graph)
          in shp_array. This is equivalent to range(len(shp_array)).

    Returns:
        - array of number_dead dead rows from all_rows.

    '''
    assert number_dead < len(all_rows) #sanity check
    random.shuffle(all_rows)
    return np.array(all_rows[:number_dead])

def DeadFirstNeighs(graph, dead_ids):
    '''
    Get E (the number of edges that connect dead firms in the actual data).
    '''
    dead_subgraph = nx.subgraph(graph, dead_ids)
    return nx.number_of_edges(dead_subgraph)

def DeadRowsPartialRand(
                        number_dead, all_rows, graph, nrand,
                        row_to_id, id_to_row
                        ):
    '''
    Get a partially random selection of n=number_dead dead rows from the
    shortest_paths array.

    We choose nrand firms from the network at random and kill them. All the
    neighbours of these dead firms are found and nrand_neighs = number_dead -
    nrand of these firms are killed. By choosing the firms partially at random
    in this way we hope to reproduce results that look more like the actual
    pattern of dead firms than when a Monte Carlo with completely random firm
    deaths is used. If we are right about this then it suggests that the real
    driving mechanism for the pattern observed is ell=1 being high (ie
    neighbouring firms dying together), and the effects at higher ell-values
    result from this.

    As a first approximation nrand = number_dead - E where E is the number of
    first neighbour edges in the real pattern of dead firms (ie the number of
    edges connecting actually dead firms in the LFN). After using this nrand the
    resulting number of first neighbour edges in the randomly selected dead
    firms is found, I call this e. If e > E (which is to be expected), then a
    lower value for nrand is chosen. The method for this calibration is discussed
    below.

    Args:
        - number_dead: number of rows we want to kill
        - all_rows: list of all the rows (which represent firms in the graph)
          in shp_array. This is equivalent to range(len(shp_array)).
        - graph: the relevant LFN
        - nrand: the number of dead firms chosen in an uncorrelated way.

    Returns:
        - array of number_dead dead rows from all_rows
    '''
    assert number_dead < len(all_rows) #sanity check
    #Get nrand dead rows
    random.shuffle(all_rows)
    deadrand = all_rows[:nrand]
    #Get all rows corresponding to first neighbours of firms in deadrand
    all_neighs = set() #container set for all the first neighs of dead nodes
    for row in deadrand:
        firm_id = row_to_id[row] #get firm ID
        neighs_id = graph.neighbors(firm_id) #get neighbours
        neighs = [id_to_row[x] for x in neighs_id] #get rows corresp. to neighs
        all_neighs = all_neighs.union(set(neighs)) #add neighs to all_neighs
    #Get nneighs dead rows, making sure that we don't choose the same row twice
    alive_neighs = list(all_neighs.difference(set(deadrand))) #get alive neighs
    random.shuffle(alive_neighs)
    nneighs = number_dead - nrand
    assert nneighs < len(alive_neighs) #sanity check
    deadrand_neighs = alive_neighs[:nneighs]
    deadrand_total = list(set(deadrand_neighs).union(set(deadrand)))
    return np.array(deadrand_total)

def MCAddRun(mc_results, mc_results_single):
    '''
    Updates the mc_results variable with the results of a Monte Carlo run.

    Args:
        - mc_results: stores all Monte Carlo results,
          mc_results[ell] = [no. pairs with ell in run 1, no. pairs with ell in
          run 2, ...]
        - mc_results_single: results of a single Monte Carlo Run, ie,
          mc_results[ell] = no. pairs of dead rows with ell in last MC run.
    '''
    assert mc_results.keys() == mc_results_single.keys() #sanity check
    for ell in mc_results_single.keys():
        mc_results[ell] += [mc_results_single[ell]]


#================================================
#---define main()-----
#================================================

def main(
        flow_years, death_years='all',
        nflowrows=None, ndeathrows=None, test=False,
        mc_runs = 0, mc_force_number_dead = 'no',
        nrand=None
        ):
        '''
        Args:
            - flow_years: format 'year1-year2'. The LFN will be created from
              flows in this time period.
            - death_years: 'all' or 'starty-endyr'. If 'all' then all firm
              deaths will be considered, if string in form stated is provided
              then only deaths in the specified years are considered.
            - nflowrows: can be used to resrict the number of lines of the flow
              file that are read. This speeds things up (since the resulting LFN
              is smaller).
            - ndeathrows: can be used to restrict the number of lines of the
              death file that are read.
            - mc_runs: the number of Monte Carlo runs to be completed.
            - mc_force_number_dead: default for number of dead firms in the
              Monte Carlo is the number that actuall died in the period.
              However, with this input you can choose the number of firms to be
              randomly chosen to die.
            - proportion_rand: proportion of dead firms in each Monte Carlo runs
              that are chosen completely at random (the remaining dead firms are
              chosen from the neighbours of the already dead firms). See docs
              for DeadRowsPartialRand.
        Outputs:
            - results: the number of pairs of dead nodes between which the
              shortest path is ell for every possible ell. Stored as dictionary
              results[ell] = no. pairs dead nodes with this ell. Saved to
              reports.
            - mc_results: similar to results, except this time we repeat over
              and over for 'dead' nodes chosen at random in the Monte Carlo.
              Also saved to reports.
            - nb if the number of rows being read in is restricted then the
              filename is prepended with 'TEST'.

        '''
        #==================================================================
        #--- 0.0. Check to see if test---
        #==================================================================
        if nflowrows!=None or ndeathrows!=None:
            test=True

        #==================================================================
        #---0.1. Make output filepaths---
        #==================================================================
        info = 'flows' + flow_years + '_deaths' + death_years
        results_filename = 'res_' + info + '.pkl'
        mc_results_filename = 'mcres_' + info + '.pkl'
        output_dir = os.path.join(project_root, 'data/processed')
        if test==True:
            mc_results_filename = 'test_' + mc_results_filename
            results_filename = 'test_' + results_filename
            output_dir = os.path.join(output_dir, 'test')
        if nrand != None:
            mc_results_filename = 'nrand' + str(nrand) +'_'+ mc_results_filename
            results_filename = 'nrand' + str(nrand) +'_'+ results_filename
        results_filepath = os.path.join(output_dir, results_filename)
        mc_results_filepath = os.path.join(output_dir, mc_results_filename)

        #check to see if output filepaths already exist:
        gen.CheckExistence(results_filepath, allow_overwrite=test)
        gen.CheckExistence(mc_results_filepath, allow_overwrite=test)

        #==================================================================
        #---1. Create LFN based on a period of flows-----
        #==================================================================
        lfn = dat.LFN(flow_years, nflow_rows=nflowrows)

        #==================================================================
        #---2. Determine dead firms based on a period of deaths.-----
        #==================================================================
        dead_ids = dat.GetDeadIds(
                        dat.deaths_filepath, death_years, ndeathrows
                        )
        print('Number dead firms: ' + str(len(dead_ids)))
        #==================================================================
        #---3. Find the shortest path between each pair of nodes in the LFN.---
        #==================================================================
        #shp = SHortest Paths.
        #Transform datastructure to array
        shp_dictofdicts = nx.all_pairs_shortest_path_length(lfn.graph)
        shp_array, row_to_id, id_to_row = SHPToArray(shp_dictofdicts)

        #==================================================================
        #---4. Find shortest path length between each pair of dead firms.----
        #==================================================================
        dead_rows = DeadRows(dead_ids, id_to_row)
        print('Number dead rows: ' + str(len(dead_rows)))
        max_ell = np.max(shp_array)
        results = Cshp.CDeadShortestPaths(
                                    dead_rows, shp_array,
                                    max_ell=max_ell
                                    )
        gen.SavePkl(results, results_filepath)

        #==================================================================
        #---5. Compare lengths of paths between dead firms with Monte Carlo ----
        #==================================================================
        #choose number of dead rows
        print('doing Monte Carlo runs')
        if mc_force_number_dead == 'no':
            number_dead = len(dead_rows)
        else:
            number_dead = mc_force_number_dead
        all_rows = id_to_row.values()
        mc_results = {}
        for i in range(-1, max_ell+1):
            mc_results[i] = []
        for i in tqdm.tqdm(range(mc_runs)): #tqdm prints out a progressbar for loop
            #get dead rows; can choose either completely or partially random
            if nrand == None:
                mc_dead_rows = DeadRowsRand(number_dead, all_rows)
            else:
                mc_dead_rows = DeadRowsPartialRand(
                                        number_dead, all_rows, g, nrand,
                                        row_to_id, id_to_row
                                        )
            #get results for single Monte Carlo Run
            mc_results_single = Cshp.CDeadShortestPaths(
                                            mc_dead_rows, shp_array,
                                            max_ell=max_ell
                                            )
            #add results for this run to overall
            MCAddRun(mc_results, mc_results_single)
            gen.SavePkl(mc_results, mc_results_filepath)
        print('---Warning: code not fully tested')
        print('---No check to see if mcres already exists with some runs',
        ' in. This would allow more runs to be added at a later date.')
        print('COMPLETE')

#================================================
#---call main-----
#================================================

if __name__ == '__main__':
    for d in ['1996-2006']:
        main(flow_years='1996-1997', death_years=d, nflowrows=200,
                mc_runs=2, nrand=None, ndeathrows=None)

#add info about number of deaths to filename
