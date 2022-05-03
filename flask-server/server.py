from email.mime import application
from flask import Flask

app = Flask(__name__)

class Graph :
    grafo={"grafo": ["hola", "adios"]}

@app.route("/grafo")
def grafo():
    return Graph.grafo
@app.route("/hola")
def hola():
    Graph.grafo={"grafo": ["dani", "rep"]}
    return Graph.grafo
@app.route("/clear")
def clear():
    Graph.grafo={"grafo": ["hola", "adios"]}
    return Graph.grafo

if __name__ == "__main__":
    app.run(debug=True)