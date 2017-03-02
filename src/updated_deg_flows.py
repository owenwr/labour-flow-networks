'''
Analyse the flows between updated degrees.

Compare the number of firms with updated degree i at the beginning of a time
interval and the number at the end. The difference is a kind of flow of updated
degree. Specifically, we can generate a matrix M[i, j] that records the flows
from updated degree i to updated degree j.

'''

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
        A : 2D numpy array
            A[i, j] is the flow from i to j during the the year.
        B : 1D numpy array
            B[i] is the number of firms with updated degree i that die.
            
    '''
    #set parameters
    t = 1997
    #get LFN
    lfn = LFN('1996-1997')
    #kill all nodes that die before year t
    #first find the nodes that are dead before t
    death_years = dat.StrFromYrs(1996, t)
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
    death_years = dat.StrFromYrs(t, t+1)
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
