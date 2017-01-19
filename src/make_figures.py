'''
Visually compare the number of pairs of dead nodes with shortest path length
ell with the results of a Monte Carlo Simulation in which dead nodes are chosen
at random.

For each ell value generate a histogram for the number of Monte Carlo runs
that produced x pairs of dead nodes with ell.

0. Get input and output filepaths.
    - inputs are results dictionaries (both actual results and Monte Carlo
        results dictionary).
    - outputs are figures
1. Generate plots
'''
import os
project_root = os.path.join(os.path.dirname(__file__), os.pardir)
import visualisation.visualise as vis
import general as gen

#------------------------------------------
#---0. Get input and output filepaths------
#------------------------------------------
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
                    #single year, deaths all years, partially random dead firms
                    ['nrand8800_mcres_flows1996-1997_deathsall.pkl',
                        'nrand8800_res_flows1996-1997_deathsall.pkl']
                    ]

#------------------------------------------
#---1. Generate plots----------------------
#------------------------------------------

for filename_pair in input_filenames:
    mc_filepath = os.path.join(input_dir, filename_pair[0])
    actual_filepath = os.path.join(input_dir, filename_pair[1])
    gen.CheckSameData(mc_filepath, actual_filepath)
    '''vis.BoxPlot(
                gen.GetPkl(mc_filepath), gen.GetPkl(actual_filepath),
                ell_values = range(0, 10),
                fig_dir=fig_dir, info=actual_filepath
                )'''
    vis.RatiosBarChart(
                        gen.GetPkl(mc_filepath), gen.GetPkl(actual_filepath),
                        ell_values = range(1, 8),
                        fig_dir=fig_dir, info=actual_filepath
                        )

#add option to produce histogram plots
