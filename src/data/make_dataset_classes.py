'''
LFN (Labour Flow Network) class definition with several methods.

Functions for retrieving and doing basic manipulation of data to yield LFNs
and sets of dead firm ids.
'''

import os
project_root = os.path.join(os.dirname(__file__), os.pardir, os.pardir)

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

        self.graph = dat.MakeLFN(flow_years, nrows=nflow_rows)
        self.filepath_info = 'flows' + flow_years
        self.AllAlive()
        self.dead_ids = set()
        self.dead_nodes = set()
        if death_years != None:
            self.filepath_info = self.filepath_info + '_deaths' + death_years
            self.dead_ids = dat.GetDeadIds(
                                    death_years=death_years, nrows=ndeath_rows
                                    )
            self.dead_nodes = set(dat.DeadInLFN(self.graph, self.dead_ids))
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
        dead_nodes = dat.DeadInLFN(self.graph, dead_ids)
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
