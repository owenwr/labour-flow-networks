'''
Functions for retrieving and doing basic manipulation of data to yield LFNs
and sets of dead firm ids.

LFN (Labour Flow Network) class definition with several methods.
'''

import os
import pandas as pd
import numpy as np
import networkx as nx

project_root = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

def YrsFromStr(years):
    '''
    Take string in format 'year1-year2' and return integers year1, year2
    '''
    year1 = int(years[:4])
    year2 = int(years[5:])
    return year1, year2

def StrFromYrs(year1, year2):
    '''
    Create string in format 'year1-year2' from integers year1, year2
    '''
    assert type(year1) == type(year2) and type(year1) == int
    return str(year1) + '-' + str(year2)

def FlowsPath(years, project_root=project_root):
    '''
    Generates filepath for flows.
    input:
        - years: flow years to be used, in form 'year1-year2'
        - project_root
    output: flows filepath
    '''
    raw_flows_dir = os.path.join(
                                project_root,
                                'data', 'raw', '16-12-2016-Mega', 'flows'
                                )
    processed_flows_dir = os.path.join(
                                        project_root, 'data', 'processed'
    )
    filename = 'flows_' + years + '.csv'
    raw_flows_filepath = os.path.join(raw_flows_dir, filename)
    processed_flows_filepath = os.path.join(processed_flows_dir, filename)
    if os.path.exists(raw_flows_filepath):
        return raw_flows_filepath
    elif os.path.exists(processed_flows_filepath):
        return processed_flows_dir
    else:
        raise IOError('File does not exist in normal places.')

deaths_filepath = os.path.join(
                                project_root,
                                'data', 'raw', '16-12-2016-Mega',
                                'dates_death.csv'
                                )

def GetDeadIds(input_filepath=deaths_filepath, death_years='all', nrows=None):
    '''
    Get firms that died in one of the years in death_years.

    Args:
        - input_filepath: filepath of dates_deat.csv with column format
        firm_id, year.
        - death_years: range of years we wish deaths in with format
        'startyr-endyr', or 'all' for all deaths. Deaths in the start year are
        included, deaths in the end year are not, so to get deaths in 2009
        require '1996-2010'.
    Output:
        - set : ids of firms that died in the specified period (or all firms
        that died).
    '''
    imported_dead = pd.read_csv(input_filepath,
                                delimiter=',', dtype=np.int, nrows=nrows)
    imported_dead = np.array(imported_dead)
    if death_years == 'all':
        dead_ids = list(imported_dead[:,0])
    else:
        dead_ids = []
        startyr, endyr = YrsFromStr(death_years)
        for i in range(len(imported_dead)):
            firm, year = imported_dead[i]
            if year in range(startyr, endyr):
                dead_ids += [firm]
    return set(dead_ids)

def DeadInLFN(graph, dead_ids):
    '''
    Get set of firms ids that are both dead and in the LFN.
    '''
    return set(dead_ids).intersection(set(graph.nodes()))

def MakeFlowsDF(flow_years, nrows=None, manual_filepath=None):
    '''
    Generates a new list of flows from two lists of flows.
    1. Check to see if flow file already exists
    2. If it doesn't exist then create it from raw data files (might be quicker
    to do creation by pre-existing merged files but that would make the code
    harder...)
    '''
    try:
        flows_filepath = FlowsPath(flow_years)
        return pd.read_csv(flows_filepath, nrows=nrows)
    except IOError:
        startyr, endyr = YrsFromStr(flow_years)
        year1, year2 = startyr, startyr+1
        df = pd.DataFrame()
        while year2 <= endyr:
            intermediate_flow_years = StrFromYrs(year1, year2)
            flows_filepath = FlowsPath(intermediate_flow_years)
            df_add = pd.read_csv(flows_filepath, nrows=nrows)
            df = df.append(df_add, ignore_index=True)
            year1 +=1
            year2 += 1
        return df

def MakeLFN(flow_years, nrows=None, manual_filepath=None, print_info=True):
    '''
    Make Labour Flow Network where one job change is sufficient for a link.

    Args:
        - input_filepath: text file with col format
         firm1_ID, firm2_ID, number
         - nrows: option to restrict the number of rows of flows read in.
         this allows for the creation of a smaller graph for testing.
    Returns:
        - networkx graph
    '''
    #note that pandas deals with the header automatically so there
    # is no need to do skiprows=1
    df = MakeFlowsDF(flow_years, manual_filepath=manual_filepath, nrows=nrows)
    g = nx.from_pandas_dataframe(
                                df,
                                source='from_firm',
                                target='to_firm',
                                edge_attr=None #take care with edge_attr='Number'
                                # it will record only the second instance of the
                                # edge (ie it will only see one flow direction)
                                )
    #set graph name to be of the form 'Flows: year1-year2'
    graph_name = 'LFN with flows: ' + flow_years + '.'
    if nrows != None:
        ' '.join([graph_name, 'Warning: Only used first', str(nrows),
        'of flows from each year\'s csv file (eg, if 1996-1997 then nrows will',
        'have been used, but if 1996-1998 then 3*nrows will have been used).'])
    g.name = graph_name
    if print_info==True:
        print(nx.info(g))
    return g

class LFN:
    '''
    Class of Labour Flow Networks.

    - Inherit from the class of networkx networks.
    - Make method: Create an LFN for the years specified
    - FilepathInfo method: return a string to be used as part of a filename
    specifying the key details of the LFN

    Node Attributes:
        'Dead': dictionary mapping every node to True if node is dead or False
        if node is alive.

    Data Attributes
        dead_nodes: set of dead nodes.
    '''

    def __init__(
                self,
                flow_years, nflow_rows=None,
                death_years=None, ndeath_rows=None
                ):
        '''
        Create LFN from specified flowyears and add corresponding filepath info.
        If deathyears provided add dead_ids and dead_nodes data attributes
        and mark dead nodes in graph as dead.
        '''

        self.graph = MakeLFN(flow_years, nrows=nflow_rows)
        self.filepath_info = 'flows' + flow_years
        self.AllAlive()
        self.dead_ids = set()
        self.dead_nodes = set()
        if death_years != None:
            self.filepath_info = self.filepath_info + '_deaths' + death_years
            self.dead_ids = GetDeadIds(
                                    death_years=death_years, nrows=ndeath_rows
                                    )
            self.dead_nodes = set(DeadInLFN(self.graph, self.dead_ids))
            self.KillNodes(self.dead_nodes)

    def PrintInfo(self):
        '''
        Print info on LFN.
        '''
        nx.info(self.graph)
        print('Death Years: ' + death_years)

    def AllAlive(self):
        '''
        Sets node attributes so that all nodes are marked as alive.
        '''
        dead_dict = dict()
        for node in self.graph.nodes():
            dead_dict[node] = False
        nx.set_node_attributes(self.graph, 'Dead', dead_dict)

    def KillNodes(self, dead_ids):
        '''
        Change node attributes for nodes in list dead_ids to Dead.
        Also updates the 'dead_nodes' list.
        '''
        dead_nodes = DeadInLFN(self.graph, dead_ids)
        new_dead_nodes = set(dead_nodes).difference(self.dead_nodes)
        #update attributes
        dead_dict = nx.get_node_attributes(self.graph, 'Dead')
        for node in new_dead_nodes:
            dead_dict[node] = True
        nx.set_node_attributes(self.graph, 'Dead', dead_dict)
        #add new dead nodes to list of dead nodes
        self.dead_nodes = self.dead_nodes.union(set(new_dead_nodes))
        self.dead_ids = self.dead_ids.union(set(dead_ids))

    def AliveNodes(self):
        '''
        Return set of nodes in LFN that are alive.
        '''
        return set(self.graph.nodes()).difference(self.dead_nodes)

    def NodeDead(self, node):
        '''
        Return True if node is dead and False if node is alive.
        '''
        return self.graph.node[node]['Dead']

    def UpdatedDegree(self, node):
        '''
        Return the updated degree of the node. That means it is
        number of neighbours of the node that are alive.
        '''
        neighs = nx.neighbors(self.graph, node)
        alive_neighs = [neigh for neigh in neighs if not self.NodeDead(neigh)]
        return len(alive_neighs)
