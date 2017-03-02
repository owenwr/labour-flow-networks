'''
Cython script for Dead Shortest Paths function. I use this since this loop
seems to take a long time in Python. I have since been told that I could
re-write this in Python but using numpy arrays in a more intelligent way to make
the looping faster.
'''

import Cython
import numpy as np
cimport numpy as np
def CDeadShortestPaths(np.ndarray dead_rows, np.ndarray shortest_paths, max_ell=40):
    '''
    Get all shortest path lengths between pairs of dead nodes using
    shortest_paths array.
    Returns dictionary with keys path lengths ell and values the number of pairs
    of nodes between which ell is the shortest path length.
    (Wrapped with Cython.)
    inputs:
        - dead_rows: 1D array listing the rows in shortest_paths that are dead.
        These rows can be found by keeping track of the Pandas index in the
        dataframe when converting dataframe to numpy array.
        - shortest_paths: 2D array giving shortest paths between each pair
        - max ell: tells us what values to put into the dictionary
    returns:
        - results: dictionary where keys are ells and values are number of pairs
        with that ell
    '''
    cdef int i, l, node1, node2
    cdef int n = np.size(dead_rows)

    results = {}
    for i in range(-1, max_ell+1):
        results[i] = 0

    for i in range(n):
        node1 = dead_rows[i]
        for i in range(n):
            node2 = dead_rows[i]
            if node1 <= node2:
                l = shortest_paths[node1][node2]
                results[l] += 1
    return results
