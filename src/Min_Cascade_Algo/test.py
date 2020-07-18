from representation import graph
from algos import cascade_calculation
from pathlib import Path
import sys

#classic argument : "./evaluation/graph_test3.txt"   sys.argv[1]

graph_file_address = Path(__file__).parent / sys.argv[1]
#graph_file_address = "D:/cascade/src/Min_Cascade_Algo/evaluation/graph_test.txt"
file = open(graph_file_address)
output_graph = graph_file_address = Path(__file__).parent / "evaluation/output_graph.txt"

#to do:
        #implement visualisation of the clusters
        #compute the cascade graph


g = graph.Graph(file.read())
new_graph, nb_moves = cascade_calculation.Calculation.possible_cascade(g)
g.actualisation(new_graph)
print("number of moves: ", nb_moves)
print(g.to_string())

file_object = open(output_graph, 'r+')
file_object.seek(0)
file_object.truncate()
file_object.write(g.to_beautiful_string())