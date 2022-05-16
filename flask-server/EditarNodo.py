
from networkx.readwrite import json_graph
import networkx as nx
import json


def crearNodo(label):
    G = subirGrafo()

    if(label == '' or G.has_node(int(label))):
        return("Nombre invalido")
    else:
        G.add_node(int(label))
        guardarGrafoJson(G)
        return "Nodo creado con éxito"

def eliminarNodo(label):
    G = subirGrafo()
    if(label == '' or not G.has_node(int(label))):
        return("No existe el nodo")
    else:
        G.remove_node(int(label))
        guardarGrafoJson(G)
        return "Nodo eliminado con éxito"


def editarNodo(label, nuevo):
    G = subirGrafo()
    if(G.has_node(int(nuevo))):
        return "El nuevo nombre ya esta en uso"
    if(G.has_node(int(label))):
        data = json_graph.node_link_data(G)
        for i in data['nodes']:
            if(i['id'] == int(label)):
                i['id'] = int(nuevo)
        for i in data['links']:
            if(i['source'] == int(label)):
                i['source'] = int(nuevo)
            if(i['target'] == int(label)):
                i['target'] = int(nuevo)
        G = json_graph.node_link_graph(data)
        guardarGrafoJson(G)
        return"Nodo editado con exito"
    else:
        return"El nodo indicado no existe"
     # if(inicio=='' and not G.has_node(inicio) and final=='' and not G.has_node(final) and G.has_edge(inicio,final)):
      #      print("Nodos invalidos")
    # else:
        #    G.remove_edge(inicio,final)


def subirGrafo():
    with open('../nuevo/src/data/data.json') as f:
        js_graph = json.load(f)
        return json_graph.node_link_graph(js_graph)


def guardarGrafoJson(G):
    with open('../nuevo/src/data/data.json', 'w') as f:
        json.dump(json_graph.node_link_data(G), f, indent=4)
