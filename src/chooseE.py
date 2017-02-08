'''
(based on the script shortest_path_lengths.py)

Chooses different values of nrand (see DeadRowsPartialRand in the
shortest_path_lengths.py file) and generates a set of dead firms using
DeadRowsPartialRand. The number of dead first neighbours, e, is the number of
pairs of firms that are in this set of dead firms and are connected by an edge
in the LFN. The actual number of dead first neighbours (ie, using the actual
dead firms, not (partially) randomly selected ones)) is denoted E.

The aim is to find the value of nrand that reproduces e=E. Or at least a value
of nrand that gets close to e=E.

1. Make LFN, get actual dead firms
2. Get actual number of dead first neighbours, E
3. Try different values of nrand and find e.
    - Choose these values in the interval [1, N-E]. The upper limit here is
    because (assuming the average degree is greater than 1) after we choose
    nrand=N-E firms then there should be at least E pairs of first neighbours.
4. Plot e vs nrand
    - By eye pick a value of nrand that generates and e close to E

n.b. there is an element of randomness: every partially random selection is just
that - random. Therefore we have to be wary of the statistics. However, if we
get a smooth curve for e vs nrand then that suggests that we have successfully
washed out the statistics.
'''
import os
import random
import matplotlib.pyplot as plt
import tqdm
import general as gen
from data import make_dataset as dat
import shortest_path_lengths as spl

project_root = os.path.join(os.path.dirname(__file__), os.pardir)

#-----------------------------------------------------------------
#----0. Args------------------------------------------------------
#-----------------------------------------------------------------
flowyears = '1996-1997'
death_years = 'all'
nflowrows = 10
ndeathrows = 10


#-----------------------------------------------------------------
#----1. Make LFN, get actual dead firms---------------------------
#-----------------------------------------------------------------
g = dat.MakeLFN(flowyears, nflowrows)
dead_ids = dat.GetDeadIds(dat.deaths_filepath, death_years, ndeathrows)
total_number_dead = len(dead_ids)
print('Number dead firms: ' + str(total_number_dead))
dead_in_LFN = set(dead_ids).intersection(set(g.nodes()))
number_dead_in_LFN = len(dead_in_LFN)
print('Number dead in LFN: ' + str(number_dead_in_LFN))


#-----------------------------------------------------------------
#----2. Get actual number of dead first neighbours, E-------------
#-----------------------------------------------------------------
E = spl.DeadFirstNeighs(g, dead_ids)
print('Number dead first neighbours: ' + str(E))


#-----------------------------------------------------------------
#----3. Try different values of nrand and find e-------------
#-----------------------------------------------------------------
ids = g.nodes()
results = dict()
results['E'] = E
number_of_repeats = 10
for nrand in tqdm.tqdm(range(8860, 8900)):
    e_list = []
    for i in range(number_of_repeats):
        random.shuffle(ids)
        deadrand = ids[:nrand]
        all_neighs = set() #container set for all first neighbours of dead firms
        for firm_id in deadrand:
            neighs_ids = g.neighbors(firm_id) #get neighbours
            all_neighs = all_neighs.union(set(neighs_ids)) #add neighs to all_neighs
            #Get nneighs dead rows, ensuring that we don't choose the same row twice
        alive_neighs = list(all_neighs.difference(set(deadrand))) #get alive neighs
        random.shuffle(alive_neighs)
        nneighs = number_dead_in_LFN - nrand
        deadrand_neighs = alive_neighs[:nneighs]
        deadrand_total = list(set(deadrand_neighs).union(set(deadrand)))
        e = spl.DeadFirstNeighs(g, deadrand_total)
        e_list += [e]
    e_avg = sum(e_list)/float(len(e_list))
    results[nrand] = e_avg
    gen.SavePkl(results, os.path.join(
                                        project_root, 'reports', 'test.pkl'
                                    ))
    '''print(E)
    print(e)
    print(nrand)
    print(nneighs)
    print(len(deadrand_total))'''


#-----------------------------------------------------------------
#----4. Plot e vs nrand-------------
#-----------------------------------------------------------------
'''plt.plot(results.keys(), results.values())
plt.xlabel('nrand')
plt.ylabel('number of first neighbour pairs, e')
plt.plot(results.keys(), E)
plt.show()'''





#--end--
