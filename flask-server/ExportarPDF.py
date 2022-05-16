from fileinput import filename
from networkx.drawing.nx_pydot import to_pydot
import graphviz
import json
from networkx.readwrite import json_graph

def guardarPDF(name):
 with open('../nuevo/src/data/data.json') as f:
        js_graph = json.load(f)
        G= json_graph.node_link_graph(js_graph)
        print(G)
         
        dot = to_pydot(G).to_string()
        
        # dot is string containing DOT notation of graph
        src = graphviz.Source(dot)
       
        a = '../nuevo/src/savesPDF/'+name
        src.view(a)


        


        

