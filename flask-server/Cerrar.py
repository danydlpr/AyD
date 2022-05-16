import json
from networkx.readwrite import json_graph
import networkx as nx

def cerrarGrafoJson():
    G=nx.Graph()
    with open('../nuevo/src/data/data.json','w') as f:    
        json.dump(json_graph.node_link_data(G),f, indent=4)     
        return "Grafo cerrado"
