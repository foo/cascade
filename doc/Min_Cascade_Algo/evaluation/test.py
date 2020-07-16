from representation import graph
from algos import cascade_calculation
from pathlib import Path


graph_file_address = Path(__file__).parent / "../evaluation/graph_test2.txt"
#graph_file_address = "../evaluation/graph_test.txt"
component1 = 0
component2 = 15

#to do : no more k and l in graph files, put a symbol in a line to say "take the previous number and add it until we reach k"
        #no reduction in number of components, add the condition X_id1_j == X_id2_j
        #implement visualisation of the clusters
        #1^17 = seventeen times the component 1
        #compute the cascade graph
        #in git, move it in cascade/src


g = graph.Graph(graph_file_address)
new_graph, nb_moves = cascade_calculation.Calculation.possible_cascade(g, component1, component2)
g.actualisation(new_graph)
print("number of moves: ", nb_moves)
print(g.to_string())

#g = graph.Graph(graph_file_address)
#g_prime = copy.deepcopy(g)
#del g
#print(g_prime.to_string())
