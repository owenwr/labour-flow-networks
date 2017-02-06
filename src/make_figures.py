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
import data.make_dataset as dat

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

bp = False
bar_ratios = False
ratios_overlay = True
degree_dist = False
cc_dist = False

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
if degree_dist == True:
    g = dat.MakeLFN('1996-1997')
    vis.DegreeDist(g)
if cc_dist == True:
    g = dat.MakeLFN('1996-1997')
    vis.CCDist(g)

#plt.show(a)

#add option to produce histogram plots
