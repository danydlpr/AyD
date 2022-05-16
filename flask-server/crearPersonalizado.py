
from networkx.readwrite import json_graph
import networkx as nx
import json


def personalizado(G,label):
    G=nx.DiGraph()
    if(label==None):
        print("Nombre invalido")
    else:
        G.add_node(label)
        guardarGrafoJson(G)
            
        
  
def guardarGrafoJson(G):
    with open('../nuevo/src/data/data.json','w') as f:    
        json.dump(json_graph.node_link_data(G),f, indent=4)       



