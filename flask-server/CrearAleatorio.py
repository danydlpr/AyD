import random
from networkx.readwrite import json_graph
import networkx as nx
import json


def limite(node):
    act = 0
    for i in range(node):
        act += i
    return act


def aleatorio(G, nodes, arc):
    if(arc > limite(nodes)):
       return "Cantidad de aristas posibles excedidas"
    else:
        for i in range(nodes):
            G.add_node(i+1)
        nodes = G.nodes
        a = []
        for x in nodes:
            a.append(x)
        for i in range(arc):
            creado = True
            while(creado):
                nI = random.choice(a)
                nD = random.choice(a)
                peso = round(random.random()*10)

                if((nI, nD) not in G.edges and (nD, nI) not in G.edges and nI != nD):
                    G.add_edge(nI, nD, weight=peso)
                    creado = False
        guardarGrafoJson(G)
        return "Grafo creado con exito"


def guardarGrafoJson(G):
    with open('../nuevo/src/data/data.json', 'w') as f:
        json.dump(json_graph.node_link_data(G), f, indent=4)
