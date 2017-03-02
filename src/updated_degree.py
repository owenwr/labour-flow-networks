'''
Look at the effect of updated degree on death.
'''

import os
import data.make_dataset_classes as dat
import collections as col
import networkx as nx
import visualisation.visualise as vis
import tqdm

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

def UpdatedDegreeRun(year1, yearend, lfn, mc=False, add_flows=True):
    '''
    Find proportion of nodes with each updated degree that die in each

    Carry out one run to get updated degrees of all dead nodes and
    all nodes. Updated degree is degree of node in LFN minus the number
    of dead neighbours of the node (ie, number of living neighbours).

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
            the number of deaths in each interval of years is found from the
            data, but the firm IDs of the dead firms are chosen at random.
        add flows : bool
            If True then every time we consider a new year we don't just kill
            the dead firms from that year, we also add any new nodes and edges
            that come from the flow data for that year.

    Returns:
        2 lists : all_updtdeg, dead_updtdeg
        dead_uptdeg is a list of the updated degrees of every firm that
        died, where the updated degree is calculated at the time of death.
        all_updtdeg is a list of the updated degrees of every firm at the end of
        each time period.

        These lists can be used to find, eg, the proportion of all firms with a
        given updated degree that died.
    '''
    lfn.AllAlive()
    results = dict()
    for year in tqdm.tqdm(range(year1, yearend)):
        #get string in form 'xxxx-yyyy' specifying death years
        year_interval = dat.StrFromYrs(year, year+1)
        if add_flows==True:
            #add any new nodes and edges from this year's flow data
            new_lfn = dat.LFN(year_interval, show_info=False)
            lfn.MergeLFNs(new_lfn, show_info=False)
        #get all nodes that are alive at the start of the time period
        all_nodes = list(lfn.AliveNodes())
        #get all firms that died during this time period
        #get ids of firms that died in this time period
        dead_ids = dat.GetDeadIds(death_years = year_interval)
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
        results[year_interval] = prop_dead
    return results

def main(flow_years, year1, yearend, number_mc_runs):
    lfn = dat.LFN(flow_years, show_info=False)
    results = UpdatedDegreeRun(year1, yearend, lfn, add_flows=True)
    mc_results = []
    for i in range(number_mc_runs):
        lfn = dat.LFN(flow_years, show_info=False)
        mc_results += [
                UpdatedDegreeRun(year1, yearend, lfn, mc=True, add_flows=True)
                ]
    #plot
    for death_years in results.keys():
        fig = plt.figure() #create figure
        ax = fig.add_subplot(1,1,1) #add axes
        updtdegs = range(1, 10)
    for updtdeg in updtdegs:
        monte_carlo = [mc_res[death_years][updtdeg][2] for mc_res in mc_results]
        actual = results[death_years][updtdeg][2]
        vis.MonteCarloBoxPlot(monte_carlo, actual, ax, info=str(updtdeg), xpos=updtdeg)
    ax.set_xlim(min(updtdegs)-1, max(updtdegs)+1)
    ax.set_ylim(0, 0.05)
    ax.set_xticklabels(updtdegs)
    ax.set_xlabel('Updated Degree. For some reason axis labels didn\'t come out right \n' \
                     'but should start at 1 on the left.')
    ax.set_ylabel('Proportion Dead')
    plt.savefig(os.path.join(
                            project_root, 'reports', 'figures', 'updated_degree_boxplots_addflows',
                            'updated_degree_boxplots' + str(death_years)+ '_addflows_' + '.png'))

if __name__ == '__main__':
    main('1996-1997', 1996, 2005, 1)
