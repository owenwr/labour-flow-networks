'''
Functions for visualising shortest paths data.

Data inputted in the form of dictionaries where keys k are path lengths and
values are (lists of, corresponding to different Monte Carlo runs) the number of
pairs of dead nodes between the shortest path is of length k.
'''
import os
project_root = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

import general as gen

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
        nodes between which the shortest path was of length ell in the ith Monte
        Carlo run
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
                    boxprops=dict(facecolor = 'k', linewidth=0, alpha = 0.8),
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

def RatiosBarChart(mc_res, actual_res, ell_values, fig_dir=None, info=None):
    '''
    Produces and saves plot of the ratio of the actual result to the average
    result of the number of pairs of firms with each ell value.

    Args:
        - mc_res: dictionary with keys as ell values and values as lists
        [ell1, ell2, ..., elli, ...] where elli is the number of pairs of dead
        nodes between which the shortest path was of length ell in the ith Monte
        Carlo run
        - actual_res: dictionary, actual_res[ell] = 'number of pairs of dead
        nodes between which shortest path is ell'
        - ell_values: list of ell values for which we want to generate box plots
        - fig_dir: directory where figures are stored
        - info: string containing the flow years and death years used for the
        data
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
    #Make bar chart
    start=min(ell_values)
    end=max(ell_values)
    plt.bar(ratios.keys()[start:end], ratios.values()[start:end], width=0.25)
    matplotlib.rcParams.update({'font.size': 8})
    plt.title(
                'Bar chart of ratios of actual number of pairs of firms with\n' \
                'each ell value to the average in a Monte Carlo with ' \
                + str(len(mc_res[0])) + ' runs.\nFlows: '
                + gen.GetFlowYears(info)
                + ',  Deaths: '
                + gen.GetDeathYears(info)
                + ' '
                + gen.GetNrand(info)
            )
    plt.ylabel('actual/mc_avg')
    plt.xlabel('ell value')
    #Get output filepath and save
    if fig_dir != None:
        filename = 'ratios_' + gen.GetFlowYears(info) + '_deaths'  \
        + gen.GetDeathYears(info) + gen.GetNrand(info) + '.png'
        plt.savefig(os.path.join(fig_dir, 'ratiosbarchart', filename))
        plt.close()
    else:
        plt.show()





#end--
