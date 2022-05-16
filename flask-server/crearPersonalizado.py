
from networkx.readwrite import json_graph
import networkx as nx
import json


def personalizado(G,label):
    G=nx.Graph()
    if(label==''):
        return "Nombre invalido"
    else:
        G.add_node(label)
        guardarGrafoJson(G)
        return "Grafo creado con éxito"
            
        
  
def guardarGrafoJson(G):
    with open('../nuevo/src/data/data.json','w') as f:    
        json.dump(json_graph.node_link_data(G),f, indent=4)       



