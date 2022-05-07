
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import json


app = Flask(__name__)
CORS(app)
class Graph :
    grafi={"grafo": ["hola", "adios"]}
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


@app.route("/grafo")
def grafo():
  
    return Graph.crearDB(Graph)

@app.route("/hola")
def hola():
    Graph.grafo={"grafo": ["dani", "rep"]}
    return Graph.grafo

@app.route("/crear",methods=['POST'])
def crear():
    nodes = request.json['nodes']
    print(nodes)
    return jsonify({'response': 'Holaaaaa'})

@app.route("/clear")
def clear():
    Graph.grafo={"grafo": ["hola", "adios"]}
    return Graph.grafo

if __name__ == "__main__":
    app.run(debug=True)

 