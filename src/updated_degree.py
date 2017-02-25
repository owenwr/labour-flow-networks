'''
Look at the effect of updated degree on death.
'''

import os
import data.make_dataset as dat
import collections as col
import networkx as nx

project_root = os.path.join(os.path.dirname(__file__), os.pardir)

def PropDead(all_count, dead_count):
    '''
    Take dictionary of dead counts and compare it to dictionary of counts for
    the entire LFN by taking ratios.
    'Overall' is the overall proportion of firms that died.
    Return dictionary of proportion dead, but also with the raw numbers.
    '''
    prop_dead = dict()
    for key in all_count.keys():
        d = dead_count[key]
        a = all_count[key]
        prop_dead[key] = (a, d, d/float(a))
    #set overall key
    d = sum(dead_count.values())
    a = sum(all_count.values())
    prop_dead['Overall'] = (a, d, d/float(a))
    return prop_dead

def UpdatedDegreeRun(year1, yearend, lfn, mc=False):
    '''
    Find proportion of nodes with each updated degree that die in each single
    year period between year1 and yearend. Updated degree is degree of node in
    LFN minus the number of dead neighbours of the node (ie, it is the number of
    living neighbours).

    More precisely, this function takes the first one year interval
    'year1-year1+1' and makes a list of the updated degree of every node in
    the LFN (since this is the first year, the updated degree is actually
    the same as the degree). It then finds the firms that died in the interval
    'year1-year1+1' and produces a list of the updated degrees of all these
    firms. The next year is then considered, 'year1+1-year1+2' and the updated
    degrees of all remaining firms are added to the list of all degrees and
    similarly the updated degrees of all firms that died in that year are added
    to the list of all dead degrees.

    Note that:
        (a) In the calculation of the updated degree of node i, nodes that
        died in the same year as node i are counted as alive.
        (b) The function returns only returns the running total of the updated
        degrees of all the firms that died in the entire 'year1-yearend' interval.

    Args:

    year1 : int
        The first year of deaths to be considered.
    yearend : int
        The last year of deaths to be considered.
    lfn : LFN
        The lfn object being considered
    mc : bool
        Specifies whether a Monte Carlo Run is desired. In a Monte Carlo run
        the number of deaths in each interval of years is found from the data,
        but the firm IDs of the dead firms are chosen at random.

    Returns:

    2 lists : all_updtdeg, dead_updtdeg
    dead_uptdeg is a list of the updated degrees of every firm that
    died, where the updated degree is calculated at the time of death. all_updtdeg
    is a list of the updated degrees of every firm at the end of each time period.

    These lists can be used to find, eg, the proportion of all firms with a given
    updated degree that died.
    '''
    lfn.AllAlive()
    results = dict()
    for year in range(year1, yearend):
        #get all nodes that are alive at the start of the time period
        all_nodes = list(lfn.AliveNodes())
        #get all firms that died during this time period
        #get string in form 'xxxx-yyyy' specifying death years
        death_years = dat.StrFromYrs(year, year+1)
        #get ids of firms that died in this time period
        dead_ids = dat.GetDeadIds(death_years = death_years)
        #get nodes that died in this time period
        dead_nodes_this_period = dat.DeadInLFN(lfn.graph, dead_ids)
        if mc==True: #if Monte Carlo run then randomise dead nodes
            n = len(dead_nodes_this_period)
            rand.shuffle(all_nodes)
            dead_nodes_this_period = all_nodes[:n]
        #get counts of how many firms with each updated degree died
        all_count = col.Counter([lfn.UpdatedDegree(node) for node in all_nodes])
        dead_count= col.Counter([lfn.UpdatedDegree(node) for node in dead_nodes_this_period])
        #turn counts into dictionary
        prop_dead = PropDead(all_count, dead_count)
        results[death_years] = prop_dead
    return results
