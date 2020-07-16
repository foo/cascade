from representation import graph
from algos import cascade_calculation


graph_file_address = "./evaluation/graph_test.txt"
component1 = 1
component2 = 3


g = graph.Graph(graph_file_address)
new_graph, nb_moves = cascade_calculation.Calculation.possible_cascade(g, component1, component2)
g.actualisation(new_graph)
print("number of moves: ", nb_moves)
print(g.to_string())

#g = graph.Graph(graph_file_address)
#g_prime = g.copy()
#del g
#print(g_prime.to_string())
