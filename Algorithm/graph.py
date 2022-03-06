from typing import List

import numpy
class Graph:
    # $ This Datastructure accounts for Multiple Edges to Same node. 
    def __init__(self, source_node:str, sink_node:str, nodes:List[str]):
        # $ Datastructure for edge from start_node to end_node would be : self.graph[start_node_id][end_node_id][edge_id]
        self.graph = []                  # adjacency matrix [u][v][id] (u->v) multi-edges, stores capacity
        self.org_graph =  []             # empty
        self.ROW = 0                     # number of vertices
        self.node_list = nodes           # list of nodes (names in str)
        self.nodes = {}                  # {node_name: node_index_in_matrix}
        self.create_graph(source_node,sink_node,nodes)
        self.flat_graph = None           # adjacency matrix [u][v] (u->v), stores capacity
        self.FLAT_E = None               # number of edges in flat_graph 

    # $ Based on Node Data Initialize the Graph Matrix 
    def create_graph(self, source_node:str, sink_node:str, node_list:List[str]):
        total_num_nodes = len(node_list)+2   # node_list and source and sink
        self.graph = [[[] for _ in range(total_num_nodes)] for _ in range(total_num_nodes)]

        # add source node
        self.nodes[source_node] = 0
        # add regular nodes
        for node_index, node in enumerate(node_list):
            self.nodes[node] = node_index+1
        # add sink node
        self.nodes[sink_node] = total_num_nodes-1

        # number of vertices
        self.ROW = total_num_nodes
    
    def get_matching_nodes(self, search_str:str):
        # returns list of nodes that contains search_str
        return [node for node in self.node_list if search_str in node]

    def get_node_id(self, node_name:str):
        # get id of a node with name node_name
        if node_name in self.nodes:
            return self.nodes[node_name]
        return None

    def set_edges(self, start_node:str, end_nodes:List[str], weights:List[int]):
        # append weights to edges from start_node to all of end_nodes
        if start_node not in self.nodes:
            return
        for i in range(len(end_nodes)):
            self.set_edge(start_node,end_nodes[i],weights[i])

    def set_edge(self, start_node:str, end_node:str, weight:int):
        # append weight to edge (start_node, end_node)
        if start_node not in self.nodes or end_node not in self.nodes:
            return 
        # print("Setting Edge  ",start_node,end_node,self.nodes[start_node],self.nodes[end_node])
        self.graph[self.nodes[start_node]][self.nodes[end_node]].append(weight)
    
    def flatten_edges(self) -> List[List[int]]:
        # calculates flat_graph, [u][v], stores total capacity
        if not self.flat_graph:
            self.flat_graph = [[sum(x) for x in row] for row in self.graph]
        return self.flat_graph

    def num_flat_edges(self):
        # calculates number of edges in flat_graph 
        if not self.FLAT_E:
            flat_graph = self.flatten_edges()
            # self.FLAT_E = self.ROW * self.ROW - sum(flat_row.count(0) for flat_row in flat_graph) 
            self.FLAT_E = self.ROW * self.ROW 
        return self.FLAT_E

    def enumerate_flat_edge(self):
        self.num_flat_edges()
        for i, row in enumerate(self.flat_graph):
            for j, cap in enumerate(row):
                if cap != 0:
                    assert cap > 0
                    yield (i,j,cap)
        
    def edge_id(self, i, j):
        return i * self.ROW + j
    def incident_matrix(self):
        # returns the incident matrix 
        # agrees with capacity vector
        # but with sentinel source and sink at the end
        self.num_flat_edges()
        mat = [[0 for _ in range(self.FLAT_E + 2)] for _ in range(self.ROW)]
        for i, row in enumerate(self.flat_graph):
            for j, cap in enumerate(row):
                edge_id = self.edge_id(i, j)
                if cap > 0: 
                    mat[i][edge_id] = -1
                    mat[j][edge_id] = 1
        return numpy.asarray(mat) 

    def capacity_vector(self):
        # returns the capacity vector
        # agrees with incident matrix
        # but no sentinel source and sink at the end
        self.num_flat_edges()
        vec = [0 for _ in range(self.FLAT_E)]
        for i, row in enumerate(self.flat_graph):
            for j, cap in enumerate(row):
                edge_id = self.edge_id(i, j)
                vec[edge_id] = cap
        return numpy.asarray(vec)

    def __repr__(self) -> str:
        return "\n".join(str(x) for x in [self.graph, \
                                         self.ROW, \
                                         self.node_list, \
                                         self.nodes])