'''
Analyse the flows between updated degrees.

Compare the number of firms with updated degree i at the beginning of a time
interval and the number at the end. The difference is a kind of flow of updated
degree. Specifically, we can generate a matrix M[i, j] that records the flows
from updated degree i to updated degree j.

We can then modify the matrix so that M[i, j] corresponds not to flows from
updated degree i to updated degree j but from *bin* i to *bin* j, where each bin
includes a range of updated degree values. If we choose the bins to be
logarithmic then a more sensible matrix can be constructed.

I'm still working on doing the binning for the matrix.

'''
import numpy as np
import matplotlib.pyplot as plt
import data.make_dataset_classes as dat


def UpdatedDegreeFlowMatrix(lfn, year=2000):
    '''
    Generate a 2D array of updated degree flows in year specified. Also
    generate 1D array of updated degrees of firms that die during the
    year.

    Matrix elements A[i, j] are the number of firms that had updated
    degree i at the start of the year and updated degree j at the end
    of the year.

    Array elements B[i] are the number of firms with updated degree i at
    the start of the year that die during the year.

    Args:
        lfn : LFN object
        year : int

    Returns:
        (a) (2D numpy array)
            A[i, j] is the flow from i to j during the the year.
        (b) (1D numpy array)
            B[i] is the number of firms with updated degree i that die.

    '''
    print('Warning: Currently Must Use year=1997 or 1998')
    #kill all nodes that die before the specified year
    #first find the nodes that are dead before the specified year
    death_years = dat.StrFromYrs(1996, year)
    dead_ids = dat.GetDeadIds(death_years=death_years)
    #then kill them
    lfn.KillNodes(dead_ids)
    #now get all nodes that are alive at the start of t
    alive_nodes = lfn.AliveNodes()
    #get the updated degree of each of these nodes
    #have nodes as keys and lists as values, where the first
    #element in the list is the updated degree at the start of t
    #and the second element is the updated degree at the end of t
    updtd_degs = dict()
    for node in alive_nodes:
        updtd_degs[node] = [lfn.UpdatedDegree(node), None]
    #now kill all nodes that die during t
    death_years = dat.StrFromYrs(year, year+1)
    dead_ids = dat.GetDeadIds(death_years=death_years)
    dead_nodes = dat.DeadInLFN(lfn.graph, dead_ids)
    lfn.KillNodes(dead_ids)
    #set updated degrees at end of t for dead firms 'Dead'
    for node in dead_nodes:
        updtd_degs[node][1] = 'Dead'
    #set updated degrees at end of t for alive firms
    for node in lfn.AliveNodes():
        updtd_degs[node][1] = lfn.UpdatedDegree(node)

    #create the array A by taking each element in the list
    #updtd_degs.values() and using the list in the form [i, j]
    #to locate an element in A and add 1 to its value. At the end
    #A will represent a count
    #updated degree pairs
    pairs = updtd_degs.values()
    #get max degree value to set size of A
    degs = [x for x in pairs if x[1] != 'Dead']
    max_deg = max([max(x) for x in degs])
    #create 2D array for tracking degree changes
    A = np.zeros((max_deg+1, max_deg+1), dtype=int)
    #create 1D array for tracking degrees of dying nodes
    B = np.zeros(max_deg+1, dtype=int)
    for pair in pairs:
        i, j = pair
        if j == 'Dead':
            B[i] += 1
        else:
            A[i, j] += 1
    return A, B

def CreateLogBins(b, upper_limit, lower_limit=-0.01):
    '''
    Return logarithmic bin edges with log bin width b.

    Lower limit is the first bin edge, unless otherwise specified this
    is set to be just below zero (so that zeros are captured in the
    first bin). Once a bin edge greater than the upper limit is created
    (or equivalently, once the upper_limit has a bin), no more bins are
    created. This function was originally written to be used with an
    Updated Degree Flow Matrix; with such matricies we set
    upper_limit = A.shape[0].

    I found that b=0.5 usually produces sensible bins.

    nb, log bin width b defined such that log(x_i+1) = log(x_i) + b.
    So x_i+1 = x_i*e^b, and the width of bin (i, i+1) w = x_i*(e^b-1)
    So the width of a bin is proportional to its lower limit.

    Args:
        - b : float
            Logarithmic bin width
        - upper_limit : float
            Largest bin edge value
        - lower_limit : float
            Smallest bin edge value

    Returns:
        - Bin edges
    '''
    #create container of bin edges and set first two edges to -0 and 1
    bin_edges = np.array([-0.01, 1])
    #add further bin edges until the upper limit is greater than the
    #set current bin edge to 1
    bin_edge = 1
    #loop until upper limit is reached
    assert upper_limit > 1
    while bin_edge < upper_limit:
        bin_edge = bin_edge * np.exp(b)
        bin_edges = np.append(bin_edges, bin_edge)
        if len(bin_edges) > 100:
            print('Too many bins')
            break
    return bin_edges

def main():
    '''
    Print out in text and as an image the matrix of updated degree flows.
    '''
    print(A[:n, :n])
    plt.matshow(A[:n, :n])

if __name__ == '__main__':
    main()
