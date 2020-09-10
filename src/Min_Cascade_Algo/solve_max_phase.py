from representation import graph, max_phase
from algos import cascade_calculation
import sys
import time
import file_manager
import numpy as np
import matplotlib.pyplot as plt
import cProfile
import pulp


k = int(sys.argv[1])
l = int(sys.argv[2])

# todos (Maciek's cleanup):
# 1. move the new code outside of phase class: two classes: RandomPhase and MaxPhase
# 2. print the actual cascades (glue the history)
# 3. print the classification of requests into phases
# nuitka3 + readme
# run infinite from k=<parameter>

def run():
    moves = []
    cascade_repartition = np.zeros(int(np.log2(k)))
    p = max_phase.MaxPhase(k, l)
    p.max_phase(k, l)

profile = False
if profile:
    if __name__ == '__main__':
        import cProfile, pstats
        profiler = cProfile.Profile()
        profiler.enable()
        run()
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime')
        stats.print_stats()
else:
    run()

