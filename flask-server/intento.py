from traceback import print_tb
import networkx as nx
from networkx.drawing.nx_pydot import to_pydot
import graphviz
from networkx.readwrite import json_graph

G = nx.DiGraph() 
G.add_node("a")
G.add_node("b")
G.remove_node("a")

G.add_edge("a","b")


print(G.remove_edge("a","b"))
   