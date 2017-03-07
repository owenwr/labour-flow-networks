'''
Script to generate summary stats and plots for the LFN data.
'''
import os
import general as gen
import data.make_dataset as dat
import pandas as pd
import matplotlib.pyplot as plt
project_root = os.path.join(os.path.dirname(__file__), os.pardir)

def main():
    #---------------------------------------------------------------------
    #---- Cumulative and Non-Cumulative Plots of Firm Deaths -------------
    #---------------------------------------------------------------------
    deaths = pd.read_csv(dat.deaths_filepath)
    deaths.hist(column='year', cumulative=True, bins=40)
    plt.savefig(os.path.join(project_root, 'reports', 'figures', 'cum_deaths.png'))
    deaths.hist(column='year', cumulative=False, bins=40)
    plt.savefig(os.path.join(project_root, 'reports', 'figures', 'deaths.png'))

if __name__ == '__main__':
    main()
