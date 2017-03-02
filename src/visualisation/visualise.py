'''
Functions for visualising shortest paths data.

Data inputted in the form of dictionaries where keys k are path lengths and
values are (lists of, corresponding to different Monte Carlo runs) the number of
pairs of dead nodes between the shortest path is of length k.
'''
import os
project_root = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
import sys
sys.path.append(project_root)

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import numpy as np
import networkx as nx
import src.general as gen

def BoxPlotInset(inset_ell_value, mc_res, actual_res, figure, axes):
    inset_xticklabels = ['$\ell = $'+str(inset_ell_value)]
    inset_monte_carlo = [mc_res[inset_ell_value]]
    inset_actual = [actual_res[inset_ell_value]]
    ax_inset = figure.add_axes(axes) # inset axes
    bp_inset = ax_inset.boxplot(
            inset_monte_carlo, patch_artist=True,
            showcaps=False,
            boxprops=dict(facecolor = 'k', linewidth=0, alpha = 0.8, zorder=-1),
            medianprops=dict(color='w'),
            showfliers=False,
            whiskerprops=dict(color='k', linestyle='-')
            )
    ax_inset.set_xticklabels(inset_xticklabels)
    ax_inset.yaxis.set_ticks_position('none')
    ax_inset.set_yticklabels([])
    ax_inset.scatter(
                    [1], inset_actual,
                    color='gray', marker = 'D', s = 30, linewidth=2
                    )
    ax_inset.grid(b=False)
    return ax_inset

def BoxPlot(mc_res, actual_res, ell_values, fig_dir=None, info=None):
    '''
    Create series of box plots for shortest path length data. ell=1 and ell=2
    boxplots are added as insets with larger scales.

    Args:
        - mc_res: dictionary with keys as ell values and values as lists
          [ell1, ell2, ..., elli, ...] where elli is the number of pairs of dead
          nodes between which the shortest path was of length ell in the ith
          Monte Carlo run
        - actual_res: dictionary, actual_res[ell] = 'number of pairs of dead
          nodes between which shortest path is ell'
        - ell_values: list of ell values for which we want to generate box plots
        - fig_dir: directory where figures are stored
        - info: string containing the flow years and death years used for the
          data

    '''
    plt.clf()
    #Check to see if there are shortest path lenghts in one dictionary that are
    #not in the other
    all_lengths = set(mc_res.keys()).union(set(actual_res.keys()))
    lengths_in_both = set(mc_res.keys()).intersection(set(actual_res.keys()))
    lengths_not_in_both = [x for x in all_lengths if x not in lengths_in_both]
    if lengths_not_in_both != []:
        for l in lengths_not_in_both:
            print('length', l, ' not in both')
    #Format data for boxplot
    xticklabels = [] #the labels on the x-axis
    monte_carlo = [] #values for y-axis for mc
    actual = [] #values for y-axis for actual
    for ell in ell_values:
        xticklabels += ['$\ell = $'+str(ell)]
        monte_carlo += [mc_res[ell]]
        actual += [actual_res[ell]]
    fig = plt.figure() #create empty figure
    #Create axes
    ax = fig.add_subplot(1, 1, 1) #main axes
    #Create boxplots
    bp = ax.boxplot(monte_carlo, patch_artist=True,
                    showcaps=False,
                    boxprops=dict(facecolor = 'red', linewidth=0, alpha = 0.8),
                    medianprops=dict(color='w'),
                    showfliers=False,
                    whiskerprops=dict(color='k', alpha=0.5, linestyle='-'))
    ax.set_xticklabels(xticklabels)
    #Plot actual results
    ax.plot([x+1 for x in ell_values], actual, color='gray', linestyle = '--' )
    ax.scatter([x+1 for x in ell_values], actual, color='gray', marker = 'D', s = 10, linewidth=2, alpha = 1)
    #Add Title and Axes Labels
    ax.set_title(
                'Comparison of results of '
                + str(len(mc_res[0]))
                + ' Monte Carlo runs with actual results.\nFlows: '
                + gen.GetFlowYears(info)
                + ',  Deaths: '
                + gen.GetDeathYears(info)
                + ' '
                + gen.GetNrand(info)
                )
    ax.set_xlabel('Length of shortest path between two dead nodes, $\ell$')
    ax.set_ylabel('Number of pairs of dead nodes with $\ell$')
    #Add inset for ell=1
    BoxPlotInset(1, mc_res, actual_res, fig, [0.15, 0.55, 0.15, 0.3])
    #Add inset for ell=2
    BoxPlotInset(2, mc_res, actual_res, fig, [0.15, 0.2, 0.15, 0.3])
    #Add inset for ell=-1 (ie no path)
    BoxPlotInset(-1, mc_res, actual_res, fig, [0.7, 0.55, 0.15, 0.3])
    #Change y lim
    ax.set_ylim(-0.01*ax.get_ylim()[1], ax.get_ylim()[1])
    #---------------------
    #Show or Save Figure
    #---------------------
    if fig_dir != None:
        save_location = os.path.join(fig_dir, 'boxplots', 'bp_flows'
        + gen.GetFlowYears(info) + '_deaths' + gen.GetDeathYears(info)
        + gen.GetNrand(info) + '.png')
        plt.savefig(save_location)
        plt.close()
    else:
        plt.show()

def GetRatios(mc_res, actual_res):
    '''
    Generates dictionary of ratios of the actual result to the average result of
    the number of pairs of firms with each ell value.

    Args:
        - mc_res: dictionary with keys as ell values and values as lists
          [ell1, ell2, ..., elli, ...] where elli is the number of pairs of dead
          nodes between which the shortest path was of length ell in the ith
          Monte Carlo run.
        - actual_res: dictionary, actual_res[ell] = 'number of pairs of dead
          nodes between which shortest path is ell'

    Returns:
        - dictionary such that dict[ell_value] = ratio

    '''
    #Get the average number of firms with each ell value from Monte Carlo
    mc_avg = dict()
    for key in mc_res.keys():
        avg = sum(mc_res[key])/float(len(mc_res[key]))
        mc_avg[key] = avg
    #Get ratio: actual/mc_avg for each ell value
    ratios = dict()
    for key in actual_res.keys():
        ratio = actual_res[key]/float(mc_avg[key])
        ratios[key] = ratio
    return ratios

def RatiosBarCharts(
                    data_list, ell_values,
                    fig_dir=None,
                    overlay=False, log=False
                    ):
    '''
    Produces and saves plot of the ratio of the actual result to the average
    result of the number of pairs of firms with each ell value.

    Args:
        - data_list: list of tuples of filepaths in format
        [(mc_res_1, actual_res_1), ..., (mc_res_n, actual_res_n)]. Filepaths
        are for pickle files that contain the dictionaries with keys as ell
        values such that:

            - mc_res_i[ell] = [n_1, n_2, ..., n_i, ...] where n_i is the
              number of pairs of dead nodes between which the shortest path is
              ell in the ith Monte Carlo run,
            - actual_res_i[ell]= 'number of pairs of dead nodes between which
              the shortest path is ell in actual LFN'

        - ell_values: list of ell values for which we want to generate bars
        - fig_dir: directory where figures are stored

    '''
    #loop over data_list
    for filepath_pair in data_list:
        mc_filepath = filepath_pair[0]
        actual_filepath = filepath_pair[1]
        #check filepaths corresponds to same flow years and death years
        gen.CheckSameData(mc_filepath, actual_filepath)
        #load dicts from pickle files
        mc_res = gen.GetPkl(mc_filepath)
        actual_res = gen.GetPkl(actual_filepath)
        #create figure and axes for plotting
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1) #first row, first column, one subplot
        #get ratios
        ratios = GetRatios(mc_res, actual_res)
        #Make bar chart
        start=min(ell_values)
        end=max(ell_values)
        axes.bar(
                ratios.keys()[start:end], ratios.values()[start:end],
                width=0.25, color='green'
                )
        #add titles, axis labels, and formatting
        matplotlib.rcParams.update({'font.size': 8})
        info=mc_filepath
        plt.title('Bar chart of ratios of actual number of pairs of firms with'\
                    '\neach ell value to the average in a Monte Carlo with ' \
                    + str(len(mc_res[0])) + ' runs.\nFlows: '
                    + gen.GetFlowYears(info)
                    + ',  Deaths: '
                    + gen.GetDeathYears(info)
                    + ' '
                    + gen.GetNrand(info)
                )
        plt.ylabel('actual/mc_avg')
        plt.xlabel('ell value')
        if log==True:
            plt.yscale('log')
            plt.xscale('log')
        #Get output filepath and save
        if fig_dir != None:
            filename = 'ratios_' + gen.GetFlowYears(info) + '_deaths'  \
            + gen.GetDeathYears(info) + gen.GetNrand(info) + '.png'
            if log==True:
                filename = 'log_' + filename
            if overlay==True:
                filename = 'overlay_' + filename
            plt.savefig(os.path.join(fig_dir, 'ratiosbarchart', filename))
            plt.close()
            plt.clf()
        else:
            plt.show()


def RatiosOverlay(
                    data_list, ell_values,
                    fig_dir=None, cal_at=None
                ):
    '''
    Plots of ratio against ell value. Overlay plots for different death years.

    Specifically, overlay each set of data in the lists [mc_res] and
    [actual_res] and rescale so that they are overlayed and the shape can be
    compared. Rescaling is done by shifting a curve up the y-axis *after* logs
    have been taken of the ratios.

    Intended to determine whether the behaviour for high ell values looks the
    same no matter how long we wait for deaths.

    Args:
        - data_list: list of tuples of filepaths in format
          [(mc_res_1, actual_res_1), ..., (mc_res_n, actual_res_n)]. Filepaths
          are for pickle files that contain the dictionaries with keys as ell
          values such that:

            - mc_res_i[ell] = [n_1, n_2, ..., n_i, ...] where n_i is the
              number of pairs of dead nodes between which the shortest path is
              ell in the ith Monte Carlo run,
            - actual_res_i[ell]= 'number of pairs of dead nodes between which
              the shortest path is ell in actual LFN'

        - ell_values: list of ell values for which we want to generate box plots
        - fig_dir: directory where figures are stored
        - cal_at: int saying which ell_value we will calibrate at

    Returns:
        - plot

    '''
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1) #first row, first column, one subplot
    first_loop = True
    for filepath_pair in data_list:
        mc_filepath = filepath_pair[0]
        actual_filepath = filepath_pair[1]
        #check filepaths corresponds to same flow years and death years
        gen.CheckSameData(mc_filepath, actual_filepath)
        #load dicts from pickle files
        mc_res = gen.GetPkl(mc_filepath)
        actual_res = gen.GetPkl(actual_filepath)
        #get ratios
        ratios = GetRatios(mc_res, actual_res)
        log_ratios = dict()
        for key in ratios.keys():
            log_ratios[key] = np.log(ratios[key])
        #set shift calibrator (or if it already exists do shift)
        if type(cal_at)==int: #check that we want calibration
            if first_loop:
                #get the ratio value against which we will cal the others
                cal_value = log_ratios[cal_at]
                cal_log_ratios = log_ratios
            else:
                #calibrate the ratios against the first data set
                cal_difference = log_ratios[cal_at] - cal_value
                cal_log_ratios = dict()
                for key in log_ratios.keys():
                    cal_log_ratios[key] = log_ratios[key] - cal_difference
                assert np.isclose(
                                    cal_log_ratios[cal_at],
                                    cal_value,
                                    rtol=1e-05, atol=1e-08
                                    )
            x = cal_log_ratios.keys()
            y = cal_log_ratios.values()
        else:
            x = log_ratios.keys()
            y = log_ratios.values()
        #add line plot
        start = min(ell_values)
        end = max(ell_values)
        info = mc_filepath
        label = 'Flows: ' + gen.GetFlowYears(info) \
                + ',  Deaths: ' \
                + gen.GetDeathYears(info) \
                + ' ' \
                + gen.GetNrand(info)
        ax.plot(
                x[start:end],
                y[start:end],
                label=label,
                linewidth=2
                )
        first_loop=False
    #add titles, axis labels, and formatting
    plt.legend(loc=4)
    matplotlib.rcParams.update({'font.size': 8})
    plt.title('Line chart showing ratios for different numbers of ' \
              'death years. With calibration at ' + str(cal_at))
    plt.show()

def DegreeDist(graph, loglog=True):
    d = nx.degree(graph).values()
    plt.hist(d, bins=1000)
    if loglog == True:
        plt.yscale('log')
        plt.xscale('log')
    plt.title('Degree Distribution.')
    plt.show()

def CCDist(graph):
    cc_graphs = nx.connected_component_subgraphs(graph)
    sizes = [len(g.nodes()) for g in cc_graphs]
    sizes.sort()
    fig, (ax, ax2) = plt.subplots(1, 2, sharey=True)
    ax.hist(sizes[:-2])
    ax2.hist(sizes)
    ax.set_xlim(0, sizes[-2])
    ax2.set_xlim(sizes[-1],)
    ax2.get_xaxis().get_major_formatter().set_useOffset(False)
    plt.xticks(rotation=90)
    plt.yscale('log')
    #turns spines off
    ax.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax.yaxis.tick_left()
    ax2.yaxis.tick_right()
    ax.tick_params(labelright='off', labelleft='on')
    #add diagonal lines
    d = 0.025 #line size param
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((1-d, 1+d), (-d, +d), **kwargs)
    ax.plot((1-d, 1+d), (1-d, 1+d), **kwargs)
    kwargs = dict(transform=ax2.transAxes, color='k', clip_on=False)
    ax2.plot((-d, +d), (-d, +d), **kwargs)
    ax2.plot((-d, +d), (1-d, 1+d), **kwargs)
    #add titles and axes
    ax.set_title('Histogram of sizes of connected components of graph.',
                {'horizontalalignment': 'left'})
    ax.set_xlabel('Component Size')
    ax.set_ylabel('Frequency')
    plt.show()

def MonteCarloBoxPlot(monte_carlo, actual, axes, info=None, xpos=1):
    '''
    Plot monte carlo results as box and whiskers plot with actual
    result superimposed.

    Args:
        monte_carlo : list of scalars
            List of the results of each monte carlo run
        actual : scalar
            Actual result.
        info : string
            Specifies what the plot is showing.
        xpos : scalar
            Specifies the position on the x-axis of the plot.

    Returns:
        Boxplot
    '''
    axes.boxplot( monte_carlo,
                showcaps=False,
                #boxprops=dict(facecolor = 'red', linewidth=0, alpha = 0.8),
                medianprops=dict(color='w'),
                showfliers=False,
                whiskerprops=dict(color='k', alpha=0.5, linestyle='-'),
                positions=[xpos]
                )
    axes.scatter([xpos], [actual], color='gray', marker = 'D', s = 10, linewidth=2,)

#end--
