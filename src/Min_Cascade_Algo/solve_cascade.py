from representation import graph, random_phase
from algos import cascade_calculation
from pathlib import Path
import sys

#classic argument : "./evaluation/graph_test3.txt"   sys.argv[1]

graph_file_address = Path(__file__).parent / "evaluation/graph_test2.txt"

#graph_file_address = "D:/cascade/src/Min_Cascade_Algo/evaluation/graph_test.txt"
file = open(graph_file_address)
output_graph = graph_file_address = Path(__file__).parent / "evaluation/output_graph.txt"

#to do:
        #compute the cascade graph
g = graph.Graph(file.read())
graph_changes, nb_moves = cascade_calculation.Calculation.possible_cascade(g)
g.apply_cascade(graph_changes)
print("number of moves: ", nb_moves)
print(g.to_string())

#file_object = open(output_graph, 'r+')
#file_object.seek(0)
#file_object.truncate()
#file_object.write(g.to_beautiful_string())
