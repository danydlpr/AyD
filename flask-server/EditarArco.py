
from networkx.readwrite import json_graph
import networkx as nx
import json

def crearArc(ini,fin,w):
    G=subirGrafo() 
    
    if(ini==None or fin==None or  yaExisteArco(G,ini,fin)):
        print("Nombre invalido")
    else:
        G.add_edge(int(ini),int(fin),weight=int(w))
        guardarGrafoJson(G)


def borrarArc(ini,fin):
    G=subirGrafo() 
    
    if(ini==None or fin==None or not G.has_edge(int(ini),int(fin))):
        print("Nombre invalido")
    else:
        G.remove_edge((int(ini),int(fin)))
        guardarGrafoJson(G)
    if(ini==None or fin==None or not G.has_edge(int(fin),int(ini))):
        print("Nombre invalido")
    else:
        G.remove_edge((int(fin),int(ini)))
        guardarGrafoJson(G)

def editArc(ini,fin,nIni,nFin,w):
    G=subirGrafo()
    if(ini==None or fin==None or nIni==None or nFin==None or  yaExisteArco(G,nFin,nIni) or  yaExisteArco(G,nIni,nFin)):
        print("Nombre invalido")
    else:
        data=json_graph.node_link_data(G)
        for i in data['links']:
            if(i['source']==int(ini) and i['target']==int(fin)):
                i['source']=int(nIni)
                i['target']=int(nFin)
                i['weight']=int(w)
            else:
                if(i['source']==int(fin) and i['target']==int(ini)):
                    i['source']=int(nFin)
                    i['target']=int(nIni)
                    i['weight']=int(w)
        G = json_graph.node_link_graph(data)        
        guardarGrafoJson(G)


def subirGrafo():
    with open('../nuevo/src/data/data.json') as f:
        js_graph = json.load(f)
        return json_graph.node_link_graph(js_graph) 

def guardarGrafoJson(G):
    with open('../nuevo/src/data/data.json','w') as f:    
        json.dump(json_graph.node_link_data(G),f, indent=4)  

def yaExisteArco(G,i,f):
    if(G.has_edge(int(i),int(f)) or G.has_edge(int(f),int(i))):
        return True
    return False
