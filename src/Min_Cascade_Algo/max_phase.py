from representation import graph, phase
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

def run():
    moves = []
    cascade_repartition = np.zeros(int(np.log2(k)))
    p = phase.Phase(k, l)
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
