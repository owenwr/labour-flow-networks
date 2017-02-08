'''
Look at how:
(i) Degree,
(ii) Sum of degrees of neighbours
correlate with death rate.

- Produce plots of proportion of firms dead against (i)-(ii).
'''

import os
import data.make_dataset as dat
import general as gen
import collections as col
import networkx as nx
import random
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

project_root = os.path.join(os.path.dirname(__file__), os.pardir)

def ProportionDead(all_count_dict, dead_count_dict):
    '''
    Take dictionary of dead counts and compare it to dictionary of counts for
    the entire LFN by taking ratios.
    Return dictionary of proportion dead.
    '''
    prop_dead = dict()
    for key in all_count_dict.keys():
        prop_dead[key] = dead_count_dict[key]/float(all_count_dict[key])
    return prop_dead

def SelectNWithoutReplacement(domain, N):
    '''
    Select N elements from the list, choosing them uniformly at random.
    '''
    random.shuffle(domain)
    return domain[:N]

def PropPlot(
            start, end,
            dead_counted, all_counted,
            prop_dead, total_prop_dead,
            feature,
            fig_dir
            ):
    '''
    Plot proportions
    Args:
        - start: first x value we want
        - end: last x value we want
        dead_counted: collections module count dict of number of dead firms with
        each value of the feature.
        all_counted: as dead_counted except for all nodes in LFN
        prop_dead: dictionary mapping feature values to proportion dead
        total_prop_dead: overall proportion of firms in the LFN that died
        feature: we examine the effect of the feature on the death rate
    '''
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(6, 9))
    #plot distributions
    ax.plot(dead_counted.keys()[start:end],
            dead_counted.values()[start:end], label='Dead')
    ax.plot(all_counted.keys()[start:end],
            all_counted.values()[start:end], label='Total LFN')
    ax.set_yscale('log')
    ax.set_ylabel('Number of firms')
    ax.legend()
    #plot propotions and average
    xvals = prop_dead.keys()[start:end]
    ax2.plot(xvals, [total_prop_dead for x in xvals], label='Average')
    ax2.plot(xvals, prop_dead.values()[start:end], label='Actual')
    ax2.set_ylabel('Proportion of Firms Dead')
    ax2.legend()
    #overall labels
    plt.xlabel(feature)
    #show figure
    plt.savefig(os.path.join(fig_dir, 'proportion_plot_' + feature))



def main(start, end):
    #----------------------------
    #---0. Input Parameters------
    #----------------------------

    death_year1 = 1996
    time_period = 10
    death_year2 = death_year1 + time_period
    death_years = dat.StrFromYrs(death_year1, death_year2)

    flow_years = '1996-1997'
    nflowrows = None

    number_mc_runs = 10

    #----------------------------
    #---1. Output Filepaths------
    #----------------------------
    fig_dir = os.path.join(project_root, 'reports', 'figures')

    #-------------------------------
    #---2. Load LFN and Deaths------
    #------------------------------
    graph = dat.MakeLFN(flow_years, nrows=nflowrows)

    dead_ids = dat.GetDeadIds(  input_filepath=dat.deaths_filepath,
                                death_years=death_years
                                )
    #get set of nodes that are both dead and in the LFN
    dead_in_LFN = dat.DeadInLFN(dead_ids, graph)

    #get total number dead in LFN
    number_dead_in_LFN = len(dead_in_LFN)

    #total propotion dead
    total_prop_dead = number_dead_in_LFN/float(nx.number_of_nodes(graph))

    #--------------------------------------
    #---3. Effect of Degree on Death------
    #--------------------------------------

    #find degrees of dead nodes and count
    dead_degrees = [graph.degree(node) for node in dead_in_LFN]
    dead_degrees_counted = col.Counter(dead_degrees)

    #find degrees of all nodes and count
    all_degrees = graph.degree().values()
    all_degrees_counted = col.Counter(all_degrees)

    #get dictionary of proportion dead
    prop_dead_degrees = ProportionDead(all_degrees_counted, dead_degrees_counted)

    #Monte Carlo
    for i in range(number_mc_runs):
        dead_degrees_mc = SelectNWithoutReplacement(all_degrees, number_dead_in_LFN)
        dead_degrees_counted_mc = col.Counter(dead_degrees_mc)

    #prop plot
    PropPlot(
            start, end,
            dead_degrees_counted, all_degrees_counted,
            prop_dead_degrees, total_prop_dead,
            'Degree',
            fig_dir
            )

    #------------------------------------------------------
    #---4. Effect of Sum of Neighbour Degrees on Death------
    #------------------------------------------------------
    #find sums of degrees of neighbours of dead nodes and count
    dead_nsum_of_neighs = []
    for node in dead_in_LFN:
        neighs = nx.neighbors(graph, node)
        dead_nsum_of_neighs += [sum(graph.degree(neighs).values())]

    dead_nsum_counted = col.Counter(dead_nsum_of_neighs)

    nsum_of_neighs = []
    #get sums of degrees of neighbours of all nodes
    for node in graph.nodes():
        neighs = nx.neighbors(graph, node)
        nsum_of_neighs += [sum(graph.degree(neighs).values())]

    all_nsum_counted = col.Counter(nsum_of_neighs)

    #get dictionary of proportion dead
    prop_dead_nsum = ProportionDead(all_nsum_counted, dead_nsum_counted)

    #Monte Carlo
    results = dict()
    for i in range(number_mc_runs):
        dead_nsum_mc = SelectNWithoutReplacement(all_degrees, number_dead_in_LFN)
        dead_nsum_counted_mc = col.Counter(dead_degrees_mc)
        results += dead_nsum_counted_mc

    #prop plot
    PropPlot(
            start, end,
            dead_nsum_counted, all_nsum_counted,
            prop_dead_nsum, total_prop_dead,
            'Sum_of_Neighbour_Degrees',
            fig_dir
            )


if __name__ == '__main__':
    main(0, 20)





#end
