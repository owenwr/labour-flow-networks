'''
Take results of the shortest_path_lengths.py script and visualise them.

More precisely, compare the actual number of pairs of dead nodes with shortest
path length ell against the ell values found in a Monte Carlo Simulation where
dead nodes are chosen at random.

Inputs
**********

Inputs are results dictionaries as decribed in (and generated by) the
shortest_path_lengths.py script. Currently, I list every one of the processed
files from shortest_path_lengths by name manually. It would be much more
efficient if I just wrote a function to pull the file names in automatically...

Outputs
**********

Three kinds of plots are possible:

1. Boxplot of the range of Monte Carlo results with the actual result plotted on
   top as a single point. This plot is meant to put the actual results into
   context - do the firms die in a way that looks different from random?
2. Bar chart where for each ell value we plot the ratio (number of firms dead
   with ell) / (average number of nodes 'dead' with ell across all Monte Carlo
   runs). As with the boxplot, this compares what we see in reality and in the
   Monte Carlo. The further the ratio is from 1, the further we are from random.
   This plot gets around the problem that the number of pairs of firms with each
   ell value changes with ell. For example, there are far more firms in the
   network with shortest path length 6 than 1. This means that when the Monte
   Carlo for ell=1 and the Monte Carlo for ell=6 are plotted on the same graph
   (as they are in the boxplots described in 1) the ell=1 results are barely
   visable due to the scale. This plot gets around the scaling problem by
   looking at ratios instead of absolute numbers.
3. Ratios overlay. Ratios plots as in 2, but this time we overlay several such
   plots so we can compare them. There is also an option to calibrate the plots,
   ie, shift them all so that they pass through the same point. This allows one
   to compare the slopes of the lines more easily.


'''
import os
project_root = os.path.join(os.path.dirname(__file__), os.pardir)
import visualisation.visualise as vis
import general as gen
import data.make_dataset as dat

def main(bp=False, bar_ratios=False, ratios_overlay=True):
    #------------------------------------------
    #---0. Get input and output filepaths------
    #------------------------------------------
    #I list every one of the processed files from shortest_path_lengths by name
    #it would be much more efficient if I just wrote a function to pull the file
    #names in automatically...

    input_dir = os.path.join(project_root, 'data', 'processed')
    fig_dir = os.path.join(project_root, 'reports', 'figures')
    #list of lists [mont-carlo filepath, actual-results filepath]
    input_filenames = [
                        #single years, deaths all
                        ['mcres_flows1996-1997_deathsall.pkl',
                            'res_flows1996-1997_deathsall.pkl'],
                        ['mcres_flows1997-1998_deathsall.pkl',
                            'res_flows1997-1998_deathsall.pkl'],
                        ['mcres_flows1998-1999_deathsall.pkl',
                            'res_flows1998-1999_deathsall.pkl'],
                        ['mcres_flows2000-2001_deathsall.pkl',
                            'res_flows2000-2001_deathsall.pkl'],
                        ['mcres_flows2001-2002_deathsall.pkl',
                            'res_flows2001-2002_deathsall.pkl'],
                        ['mcres_flows2002-2003_deathsall.pkl',
                            'res_flows2002-2003_deathsall.pkl'],
                        ['mcres_flows2003-2004_deathsall.pkl',
                            'res_flows2003-2004_deathsall.pkl'],
                        ['mcres_flows2004-2005_deathsall.pkl',
                            'res_flows2004-2005_deathsall.pkl'],
                        #two years, deaths all
                        ['mcres_flows1999-2001_deathsall.pkl',
                            'res_flows1999-2001_deathsall.pkl'],
                        #single years, deaths 1 year
                        ['mcres_flows1996-1997_deaths1996-1997.pkl',
                            'res_flows1996-1997_deaths1996-1997.pkl'],
                        #single years, deaths two years
                        ['mcres_flows1996-1997_deaths1996-1998.pkl',
                            'res_flows1996-1997_deaths1996-1998.pkl'],
                        ['mcres_flows1997-1998_deaths1997-1999.pkl',
                            'res_flows1997-1998_deaths1997-1999.pkl'],
                        ['mcres_flows1998-1999_deaths1998-2000.pkl',
                            'res_flows1998-1999_deaths1998-2000.pkl'],
                        #single years, deaths 3 years
                        ['mcres_flows1996-1997_deaths1996-1999.pkl',
                            'res_flows1996-1997_deaths1996-1999.pkl'],
                        ['mcres_flows1998-1999_deaths1998-2001.pkl',
                            'res_flows1998-1999_deaths1998-2001.pkl'],
                        #single years, deaths 4 years
                        ['mcres_flows1996-1997_deaths1996-2000.pkl',
                            'res_flows1996-1997_deaths1996-2000.pkl'],
                        ['mcres_flows1998-1999_deaths1998-2002.pkl',
                            'res_flows1998-1999_deaths1998-2002.pkl'],
                        #single years, deaths 5 years
                        ['mcres_flows1996-1997_deaths1996-2001.pkl',
                            'res_flows1996-1997_deaths1996-2001.pkl'],
                        ['mcres_flows1998-1999_deaths1998-2003.pkl',
                            'res_flows1998-1999_deaths1998-2003.pkl'],
                        #single years, deaths 6 years
                        ['mcres_flows1996-1997_deaths1996-2002.pkl',
                            'res_flows1996-1997_deaths1996-2002.pkl'],
                        ['mcres_flows1998-1999_deaths1998-2004.pkl',
                            'res_flows1998-1999_deaths1998-2004.pkl'],
                        #single years, deaths 7 years
                        ['mcres_flows1996-1997_deaths1996-2003.pkl',
                            'res_flows1996-1997_deaths1996-2003.pkl'],
                        ['mcres_flows1998-1999_deaths1998-2005.pkl',
                            'res_flows1998-1999_deaths1998-2005.pkl'],
                        #single years, deaths 8 years
                        ['mcres_flows1996-1997_deaths1996-2004.pkl',
                            'res_flows1996-1997_deaths1996-2004.pkl'],
                        #single years, deaths 9 years
                        ['mcres_flows1996-1997_deaths1996-2005.pkl',
                            'res_flows1996-1997_deaths1996-2005.pkl'],
                        #single years, deaths 10 years
                        ['mcres_flows1996-1997_deaths1996-2006.pkl',
                            'res_flows1996-1997_deaths1996-2006.pkl'],
                        #single years, deaths 11 years
                        ['mcres_flows1996-1997_deaths1996-2007.pkl',
                            'res_flows1996-1997_deaths1996-2007.pkl'],
                        #single years, deaths 12 years
                        ['mcres_flows1996-1997_deaths1996-2008.pkl',
                            'res_flows1996-1997_deaths1996-2008.pkl'],
                        #single years, deaths 13 years
                        ['mcres_flows1996-1997_deaths1996-2009.pkl',
                            'res_flows1996-1997_deaths1996-2009.pkl'],
                        #single years, deaths 14 years
                        ['mcres_flows1996-1997_deaths1996-2010.pkl',
                            'res_flows1996-1997_deaths1996-2010.pkl'],
                        #single year, deaths all years, partially random dead firms
                        ['nrand8800_mcres_flows1996-1997_deathsall.pkl',
                            'nrand8800_res_flows1996-1997_deathsall.pkl']
                        ]

    same_flows = [
                        #single years, deaths all
                        ['mcres_flows1996-1997_deathsall.pkl',
                            'res_flows1996-1997_deathsall.pkl'],
                        #single years, deaths 1 year
                        ['mcres_flows1996-1997_deaths1996-1997.pkl',
                            'res_flows1996-1997_deaths1996-1997.pkl'],
                        #single years, deaths two years
                        ['mcres_flows1996-1997_deaths1996-1998.pkl',
                            'res_flows1996-1997_deaths1996-1998.pkl'],
                        #single years, deaths 3 years
                        ['mcres_flows1996-1997_deaths1996-1999.pkl',
                            'res_flows1996-1997_deaths1996-1999.pkl'],
                        #single years, deaths 4 years
                        ['mcres_flows1996-1997_deaths1996-2000.pkl',
                            'res_flows1996-1997_deaths1996-2000.pkl'],
                        #single years, deaths 5 years
                        ['mcres_flows1996-1997_deaths1996-2001.pkl',
                            'res_flows1996-1997_deaths1996-2001.pkl'],
                        #single years, deaths 6 years
                        ['mcres_flows1996-1997_deaths1996-2002.pkl',
                            'res_flows1996-1997_deaths1996-2002.pkl'],
                        #single years, deaths 7 years
                        ['mcres_flows1996-1997_deaths1996-2003.pkl',
                            'res_flows1996-1997_deaths1996-2003.pkl'],
                        #single years, deaths 8 years
                        ['mcres_flows1996-1997_deaths1996-2004.pkl',
                            'res_flows1996-1997_deaths1996-2004.pkl'],
                        #single years, deaths 9 years
                        ['mcres_flows1996-1997_deaths1996-2005.pkl',
                            'res_flows1996-1997_deaths1996-2005.pkl'],
                        #single years, deaths 10 years
                        ['mcres_flows1996-1997_deaths1996-2006.pkl',
                            'res_flows1996-1997_deaths1996-2006.pkl'],
                        #single years, deaths 11 years
                        ['mcres_flows1996-1997_deaths1996-2007.pkl',
                            'res_flows1996-1997_deaths1996-2007.pkl'],
                        #single years, deaths 12 years
                        ['mcres_flows1996-1997_deaths1996-2008.pkl',
                            'res_flows1996-1997_deaths1996-2008.pkl'],
                        #single years, deaths 13 years
                        ['mcres_flows1996-1997_deaths1996-2009.pkl',
                            'res_flows1996-1997_deaths1996-2009.pkl'],
                        #single years, deaths 14 years
                        ['mcres_flows1996-1997_deaths1996-2010.pkl',
                            'res_flows1996-1997_deaths1996-2010.pkl'],
                        #single year, deaths all years, partially random dead firms
                        ['nrand8800_mcres_flows1996-1997_deathsall.pkl',
                            'nrand8800_res_flows1996-1997_deathsall.pkl']
                        ]

    same_flows_every_third_year = [
                        #single years, deaths all
                        ['mcres_flows1996-1997_deathsall.pkl',
                            'res_flows1996-1997_deathsall.pkl'],
                        #single years, deaths 4 years
                        ['mcres_flows1996-1997_deaths1996-2000.pkl',
                            'res_flows1996-1997_deaths1996-2000.pkl'],
                        #single years, deaths 7 years
                        ['mcres_flows1996-1997_deaths1996-2003.pkl',
                            'res_flows1996-1997_deaths1996-2003.pkl'],
                        #single years, deaths 10 years
                        ['mcres_flows1996-1997_deaths1996-2006.pkl',
                            'res_flows1996-1997_deaths1996-2006.pkl'],
                        #single years, deaths 13 years
                        ['mcres_flows1996-1997_deaths1996-2009.pkl',
                            'res_flows1996-1997_deaths1996-2009.pkl'],
                        #single years, deaths 14 years
                        ['mcres_flows1996-1997_deaths1996-2010.pkl',
                            'res_flows1996-1997_deaths1996-2010.pkl'],
                        #single year, deaths all years, partially random dead firms
                        ['nrand8800_mcres_flows1996-1997_deathsall.pkl',
                            'nrand8800_res_flows1996-1997_deathsall.pkl']
                        ]

    looking_at_nrand =[
                        #single years, deaths all
                        ['mcres_flows1996-1997_deathsall.pkl',
                            'res_flows1996-1997_deathsall.pkl'],
                        #single year, deaths all years, partially random dead firms
                        ['nrand8800_mcres_flows1996-1997_deathsall.pkl',
                            'nrand8800_res_flows1996-1997_deathsall.pkl']
                        ]

    #---make filepaths---
    #join the filenames entered in manually above to the filepath of the folder
    #the data is contained in.
    #filename_pairs = input_filenames
    filename_pairs = looking_at_nrand
    #filename_pairs = [same_flows[i] for i in [0, 9]]
    input_filepaths = []
    for filename_pair in filename_pairs:
        mc_filepath = os.path.join(input_dir, filename_pair[0])
        actual_filepath = os.path.join(input_dir, filename_pair[1])
        filepath_pair = (mc_filepath, actual_filepath)
        input_filepaths += [filepath_pair]

    #------------------------------------------
    #---1. Generate plots----------------------
    #------------------------------------------

    if bp==True:
        for filename_pair in input_filenames[:1]:
            mc_filepath = os.path.join(input_dir, filename_pair[0])
            actual_filepath = os.path.join(input_dir, filename_pair[1])
            gen.CheckSameData(mc_filepath, actual_filepath)
            vis.BoxPlot(
                        gen.GetPkl(mc_filepath), gen.GetPkl(actual_filepath),
                        ell_values = range(0, 10),
                        fig_dir=fig_dir, info=actual_filepath
                        )
    if bar_ratios==True:
        vis.RatiosBarCharts(
                            input_filepaths,
                            ell_values = range(1, 8),
                            fig_dir=fig_dir, log=False
                            )
    if ratios_overlay==True:
        vis.RatiosOverlay(  input_filepaths,
                            ell_values = range(0, 13),
                            fig_dir=fig_dir, cal_at=1
                            )

#add option to produce histogram plots


if __name__ == '__main__':
    main()