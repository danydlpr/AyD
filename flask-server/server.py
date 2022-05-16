
from cProfile import label
import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from networkx.readwrite import json_graph
import json
import pandas as pd
import networkx as nx
import CrearAleatorio
import crearPersonalizado
import Cerrar
import EditarNodo
import ExportarPDF
import ExportarPNG
from networkx.drawing.nx_pydot import to_pydot
import EditarArco

app = Flask(__name__)
CORS(app)
G = nx.DiGraph()
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
            a = '../nuevo/src/saves/save' + \
                str(round(random.random()*100))+".json"
            with open(a, 'w') as f:
                json.dump(data, f, indent=4)
                numg += 1

    def guardarComo(self, name):
        with open('../nuevo/src/data/data.json') as file:
            data = json.load(file)
            a = '../nuevo/src/saves/'+name+".json"
            with open(a, 'w') as f:
                json.dump(data, f, indent=4)

    def guardarExcel(self, name):
        with open('../nuevo/src/data/data.json') as file:
            data = json.load(file)
            a = '../nuevo/src/savesExcel/'+name+".xlsx"
            df = pd.DataFrame.from_dict(data, orient='index')
            df.transpose()
            df.to_excel(a)
    def abrir(self,name):
         with open('../nuevo/src/saves/'+name+'.json') as file:
            data = json.load(file)
            with open('../nuevo/src/data/data.json', 'w') as f:
                json.dump(data, f, indent=4)

    


@app.route("/grafo")
def grafo():

    return Graph.crearDB(Graph)


@app.route("/guardar", methods=['POST'])
def guardar():
    Graph.guardarGrafo(Graph, numg)
    Graph.crearDB(Graph)
    return "hoña"


@app.route("/guardarComo", methods=['POST'])
def guardarComo():
    name = request.json['name']
    Graph.guardarComo(Graph, name)
    Graph.crearDB(Graph)
    return "hoña"


@app.route("/exportarComoExcel", methods=['POST'])
def guardarComoExcel():
    name = request.json['name']
    Graph.guardarExcel(Graph, name)
    return "hoña"
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
    G = nx.DiGraph()
    nodes = request.json['nodes']

    arcos = request.json['arcos']
   
    CrearAleatorio.aleatorio(G, int(nodes), int(arcos))
    return "hoña"
@app.route("/editarNodo", methods=['POST'])
def editarNodo():
    
    label = request.json['label']

    nuevo = request.json['nuevo']
    EditarNodo.editarNodo(label,nuevo)
    
    return "hoña"

@app.route("/nuevoNodo", methods=['POST'])
def nuevoNodo():
    label = request.json['name']
    EditarNodo.crearNodo(label)
    return "fd"
    
@app.route("/eliminarNodo", methods=['POST'])
def eliminarNodo():
    label = request.json['name']
    EditarNodo.eliminarNodo(label)

    return "hoña"
@app.route("/editarArco", methods=['POST'])
def editarArco():
    
    inicio = request.json['inicio']
    w=request.json['weight']
    fin = request.json['fin']
    nuevoInicio = request.json['nuevoInicio']
    nuevoFin = request.json['nuevoFin']
    EditarArco.editArc(inicio,fin,nuevoInicio,nuevoFin,w)
    
    return "hoña"

@app.route("/nuevoArco", methods=['POST'])
def nuevoArco():
    inicio = request.json['inicio']
    w=request.json['weight']
    fin = request.json['fin']
    EditarArco.crearArc(inicio,fin,w)
    return "fd"
    
@app.route("/eliminarArco", methods=['POST'])
def eliminarArco():
    inicio = request.json['inicio']

    fin = request.json['fin']
    EditarArco.borrarArc(inicio,fin)

    return "hoña"
@app.route("/crearPer", methods=['POST'])
def crearPer():
    label = request.json['name']
    crearPersonalizado.personalizado(G, label)

    return "hoña"


@app.route("/clear")
def clear():
    Cerrar.cerrarGrafoJson()
    return "hoña"


@app.route("/abrir", methods=['POST'])
def abrir():
    label = request.json['archivo']
    print(label)
    Graph.abrir(Graph,label)

    return "hoña"


if __name__ == "__main__":
    app.run(debug=True)
