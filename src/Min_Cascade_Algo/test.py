from representation import graph
from algos import cascade_calculation
from pathlib import Path


graph_file_address = Path(__file__).parent / "./evaluation/graph_test.txt"
#to do:
        #implement visualisation of the clusters
        #compute the cascade graph


g = graph.Graph(graph_file_address)
new_graph, nb_moves = cascade_calculation.Calculation.possible_cascade(g)
g.actualisation(new_graph)
print("number of moves: ", nb_moves)
print(g.to_string())