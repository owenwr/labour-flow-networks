'''
Script to get shortest path lengths (what I call ell values) between pairs
of dead nodes in a Labour Flow Network. Both the nodes that actually die and
a Monte Carlo are produced.

1. Create LFN based on a period of flows.
2. Determine dead firms based on a period of deaths.
3. Find the shortest path between each pair of nodes in the LFN.
4. Find shortest path length between each pair of dead firms.
5. Compare lengths of paths between dead firms with Monte Carlo Simulation
where dead firms are picked at random (but the total number dying is fixed).
'''

#================================================
#---imports and env variables-----
#================================================
import os
import numpy as np
import networkx as nx
import pandas as pd
import tqdm
import random
import pickle as pkl
from data.make_dataset import YrsFromStr, MakeLFN

import Cython
import pyximport
pyximport.install(setup_args={ "include_dirs":np.get_include()})
import C_shortest_path_lengths as Cshp

project_root = os.path.join(os.path.dirname(__file__), os.pardir)

#================================================
#---define functions-----
#================================================

def GetDeadIds(input_filepath, death_years='all', nrows=None):
    '''
    Get firms that died in one of the years in death_years.
    Inputs:
        - input_filepath: filepath of dates_deat.csv with column format
        firm_id, year.
        - death_years: range of years we wish deaths in with format
        'startyr-endyr', or 'all' for all deaths.
    Output:
        - ids of firms that died in the specified period (or all firms
        that died).
    '''
    imported_dead = pd.read_csv(input_filepath,
                                delimiter=',', dtype=np.int, nrows=nrows)
    imported_dead = np.array(imported_dead)
    if death_years == 'all':
        dead_ids = list(imported_dead[:,0])
    else:
        dead_ids = []
        startyr, endyr = YrsFromStr(death_years)
        for i in range(len(imported_dead)):
            firm, year = imported_dead[i]
            if year in range(startyr, endyr):
                dead_ids += [firm]
    return dead_ids

def SHPToArray(shp_dictofdicts):
    '''
    Transform dict of dicts to array plus dictionay mapping firm IDs to row
    numbers and tuple mapping row numbers to firm IDs.
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
    Take ids of dead firms and return array of rows of shp_array that are dead
    !!note that firm ids for firms that are not in the LFN are discarded!!
    '''
    dead_ids = set(dead_ids)
    ids_in_g = set(id_to_row.keys())
    #get ids that are both in g and are dead.
    dead_ids_in_g = dead_ids.intersection(ids_in_g)
    return np.array([id_to_row[x] for x in dead_ids_in_g])

def DeadRowsRand(number_dead, all_rows):
    '''
    Get a random selection of n=number_dead dead rows.
    Note that all_rows is a mutable type and is passed by value so this function
    changed it, that doesn't matter though - it's just shuffling the order.
    Inputs:
        - number_dead: number of rows we want to kill
        - all_rows: list of all the rows (which represent firms in the graph).
        This is equivalent to range(len(shp_array))
    Returns:
        - array of number_dead dead rows from all_rows
    '''
    assert number_dead < len(all_rows) #sanity check
    random.shuffle(all_rows)
    return np.array(all_rows[:number_dead])

def MCAddRun(mc_results, mc_results_single):
    '''
    Updates the mc_results variable with the results of a Monte Carlo run.
    Inputs:
        - mc_results: stores all Monte Carlo results,
        mc_results[ell] = [no. pairs with ell in run 1, no. pairs with ell in
        run 2, ...]
        - mc_results_single: results of a single Monte Carlo Run, ie,
        mc_results[ell] = no. pairs of dead rows with ell in last MC run.
    '''
    assert mc_results.keys() == mc_results_single.keys() #sanity check
    for ell in mc_results_single.keys():
        mc_results[ell] += [mc_results_single[ell]]

def SavePkl(obj, filepath):
    #if os.path.exists(filepath):
    #    raise IOError('File already exists')
    f = open(filepath, 'wb')
    pkl.dump(obj, f)
    f.close()


#================================================
#---define main()-----
#================================================

def main(flow_years, death_years='all',
        nflowrows=None, ndeathrows=None,
        mc_runs = 0, mc_force_number_dead = 'no'):
        '''
        Inputs:
            - flow_years: format 'year1-year2'. The LFN will be created from
            flows in this time period.
            - death_years: 'all' or 'starty-endyr'. If 'all' then all firm deaths
            will be considered, if string in form stated is provided then only
             deaths in the specified years are considered.
            - nflowrows: can be used to resrict the number of lines of the flow
            file that are read. This speeds things up (since the resulting LFN
            is smaller).
            - ndeathrows: can be used to restrict the number of lines of the
            death file that are read.
            - mc_runs: the number of Monte Carlo runs to be completed
            - mc_force_number_dead: default for number of dead firms in the
            Monte Carlo is the number that actuall died in the period. However,
            with this input you can choose the number of firms to be randomly
            chosen to die.
        Outputs:
        '''
        #==================================================================
        #---0. Make output filepaths---
        #==================================================================
        info = 'flows' + flow_years + '_deaths' + death_years
        results_filename = 'res_' + info + '.pkl'
        mc_results_filename = 'mcres_' + info + '.pkl'
        reports_dir = os.path.join(project_root, 'reports')
        results_filepath = os.path.join(reports_dir, results_filename)
        mc_results_filepath = os.path.join(reports_dir, mc_results_filename)

        #==================================================================
        #---1. Create LFN based on a period of flows-----
        #==================================================================
        g = MakeLFN(flow_years, nflowrows)

        #==================================================================
        #---2. Determine dead firms based on a period of deaths.-----
        #==================================================================
        deaths_filepath = os.path.join(
                                        project_root,
                                        'data', 'raw', '16-12-2016-Mega',
                                        'dates_death.csv'
                                        )
        dead_ids = GetDeadIds(deaths_filepath, death_years, ndeathrows)

        #==================================================================
        #---3. Find the shortest path between each pair of nodes in the LFN.---
        #==================================================================
        #shp = SHortest Paths.
        #Transform datastructure to array
        shp_dictofdicts = nx.all_pairs_shortest_path_length(g)
        shp_array, row_to_id, id_to_row = SHPToArray(shp_dictofdicts)

        #==================================================================
        #---4. Find shortest path length between each pair of dead firms.----
        #==================================================================
        dead_rows = DeadRows(dead_ids, id_to_row)
        max_ell = np.max(shp_array)
        results = Cshp.CDeadShortestPaths(
                                    dead_rows, shp_array,
                                    max_ell=max_ell
                                    )
        SavePkl(results, results_filepath)

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
            mc_dead_rows = DeadRowsRand(number_dead, all_rows)
            #get results for single Monte Carlo Run
            mc_results_single = Cshp.CDeadShortestPaths(
                                            mc_dead_rows, shp_array,
                                            max_ell=max_ell
                                            )
            #add results for this run to overall
            MCAddRun(mc_results, mc_results_single)
            SavePkl(mc_results, mc_results_filepath)
        print('Warning: code not fully tested')
        print('Warning: No check for file over-write being done in SavePkl.')
        print('Warning: No check to see if mcres already exists with some runs',
        ' in. This would allow more runs to be added at a later date.')

#================================================
#---run main-----
#================================================

if __name__ == '__main__':
    for flow_years in ['1996-2000']:
        main(flow_years, nflowrows=100, mc_runs=100)
