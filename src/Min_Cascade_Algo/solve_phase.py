from representation import graph, phase
from algos import cascade_calculation
from pathlib import Path
import sys
import time

# k = sys.argv[1]
# l = sys.argv[2]
k = 100
l = 2
trial_number = 500
output_graph = graph_file_address = Path(__file__).parent / "evaluation/output_graph.txt"

best_score = 0
best_phases = []

for i in range(trial_number):
    t0 = time.time()
    p = phase.Phase(k, l)
    p.start_phase("random")
    if best_score < sum(p.cascade_costs):
        best_score = sum(p.cascade_costs)
        best_phases.clear()
        best_phases.append(p.history)
    elif best_score == sum(p.cascade_costs):
        best_phases.append(p.history)
    duration = time.time() - t0
    remaining_time = (trial_number - i) * duration
    hours = remaining_time//3600
    minutes = (remaining_time - hours*3600)//60
    print(i * 100 / trial_number, "%   rem. time : ", hours, "h ", minutes, "m   best : ", best_score)

for s in best_phases:
    for s2 in s:
        print(s2)

print("best score : ", best_score)

