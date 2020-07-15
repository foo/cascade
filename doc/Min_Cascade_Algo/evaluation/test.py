from reprentation import graph
from algos import cascade_calculation

graph_file_address = "graph_test.txt"


g = graph.Graph(graph_file_address)
new_graph = cascade_calculation.Calculation.possible_cascade(g, 0, 2)
g.actualisation(new_graph)
print(g.to_string())
