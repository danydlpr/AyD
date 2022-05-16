from traceback import print_tb
import networkx as nx
from networkx.drawing.nx_pydot import to_pydot
import graphviz
from networkx.readwrite import json_graph

G = nx.Graph() 
G.add_node("a")
G.add_node("b")
G.add_node("c")


G.add_edge("a","b")

print(nx.adjacency_matrix(G,nodelist=sorted(G.nodes()), weight='weight').todense())

   