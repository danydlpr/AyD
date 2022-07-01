
import random
from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient
import json
from algoritmos import que2
import pandas as pd
import networkx as nx
import CrearAleatorio
import crearPersonalizado
import Cerrar
import EditarNodo
import ExportarPDF
import ExportarPNG
import EditarArco
from networkx.readwrite import json_graph
app = Flask(__name__)
CORS(app)
G = nx.Graph()
numg = 0


class Graph:

    grafi = {"grafo": ["hola", "adios"]}
    global myCollection

    def guardarJson(self):
        with open('../nuevo/src/data/data.json') as file:
            data = json.load(file)

        result = self.myCollection.insert_one(data)
        return self.grafi

    def crearDB(self):
        client = MongoClient('localhost', 27017)

        db = client.flask_db
        db = client["Grafos"]
        self.myCollection = db["Jsons"]
        self.guardarJson(self)
        return self.grafi

    def guardarGrafo(self, numg):
        with open('../nuevo/src/data/data.json') as file:
            data = json.load(file)
            num=str(round(random.random()*100))
            a = '../nuevo/src/saves/save' + \
                num+".json"
            with open(a, 'w') as f:
                json.dump(data, f, indent=4)
                return"Guardado exitosamente como: save"+str(num)+".json"
    def matrix(self):
        with open('../nuevo/src/data/data.json') as f:
            js_graph = json.load(f)
            G= json_graph.node_link_graph(js_graph) 
            return nx.adjacency_matrix(G,nodelist=sorted(G.nodes()), weight='weight').todense()

    def guardarComo(self, name):
        with open('../nuevo/src/data/data.json') as file:
            data = json.load(file)
            a = '../nuevo/src/saves/'+name+".json"
            with open(a, 'w') as f:
                json.dump(data, f, indent=4)
                return"Guardado exitosamente como: "+str(name)+".json"
                

    def guardarExcel(self, name):
        with open('../nuevo/src/data/data.json') as file:
            data = json.load(file)
            a = '../nuevo/src/savesExcel/'+name+".xlsx"
            df = pd.DataFrame.from_dict(data, orient='index')
            df.transpose()
            df.to_excel(a)
            return "Guardado como"+name+".xlsx con exito"

    def abrir(self, name):
        with open('../nuevo/src/saves/'+name+'.json') as file:
            data = json.load(file)
            with open('../nuevo/src/data/data.json', 'w') as f:
                json.dump(data, f, indent=4)
                return "Grafo abierto"


@app.route("/grafo")
def grafo():

    return Graph.crearDB(Graph)


@app.route("/guardar", methods=['POST'])
def guardar():
    msm=Graph.guardarGrafo(Graph, numg)
    Graph.crearDB(Graph)
    return msm


@app.route("/guardarComo", methods=['POST'])
def guardarComo():
    name = request.json['name']
    msm=Graph.guardarComo(Graph, name)
    Graph.crearDB(Graph)
    return msm

@app.route("/que", methods=['POST'])
def que():
    a,b,c =que2.QUEYRANNE(Graph.matrix(Graph),que2.log_det)
    for i in a :
        EditarNodo.eliminarNodo(str(i))
    
    return str("Se cortaron los nodos: "+str(a))



@app.route("/matrix", methods=['POST'])
def matrix():
    
    return str(Graph.matrix(Graph))


@app.route("/exportarComoExcel", methods=['POST'])
def guardarComoExcel():
    name = request.json['name']
    
    return Graph.guardarExcel(Graph, name)


@app.route("/exportarComoPDF", methods=['POST'])
def guardarComoPDF():

    name = request.json['name']

    ExportarPDF.guardarPDF(name)
    return "hoña"


@app.route("/exportarComoPNG", methods=['POST'])
def guardarComoPNG():

    name = request.json['name']

    ExportarPNG.guardarPNG(name)
    return "hoña"


@app.route("/crearAl", methods=['POST'])
def crear():
    G = nx.Graph()
    nodes = request.json['nodes']

    arcos = request.json['arcos']

    return CrearAleatorio.aleatorio(G, int(nodes), int(arcos))


@app.route("/editarNodo", methods=['POST'])
def editarNodo():

    label = request.json['label']

    nuevo = request.json['nuevo']
    

    return EditarNodo.editarNodo(label, nuevo)


@app.route("/nuevoNodo", methods=['POST'])
def nuevoNodo():
    label = request.json['name']
    
    return EditarNodo.crearNodo(label)


@app.route("/eliminarNodo", methods=['POST'])
def eliminarNodo():
    label = request.json['name']
    return EditarNodo.eliminarNodo(label)


@app.route("/editarArco", methods=['POST'])
def editarArco():

    inicio = request.json['inicio']
    w = request.json['weight']
    fin = request.json['fin']
    nuevoInicio = request.json['nuevoInicio']
    nuevoFin = request.json['nuevoFin']
    return EditarArco.editArc(inicio, fin, nuevoInicio, nuevoFin, w)


@app.route("/nuevoArco", methods=['POST'])
def nuevoArco():
    inicio = request.json['inicio']
    w = request.json['weight']
    fin = request.json['fin']
    return EditarArco.crearArc(inicio, fin, w)


@app.route("/eliminarArco", methods=['POST'])
def eliminarArco():
    inicio = request.json['inicio']
    fin = request.json['fin']
    return EditarArco.borrarArc(inicio, fin)


@app.route("/crearPer", methods=['POST'])
def crearPer():
    label = request.json['name']
    return crearPersonalizado.personalizado(G, label)


@app.route("/clear")
def clear():

    return Cerrar.cerrarGrafoJson()


@app.route("/abrir", methods=['POST'])
def abrir():
    label = request.json['archivo']
    return Graph.abrir(Graph, label)


if __name__ == "__main__":
    app.run(debug=True)
