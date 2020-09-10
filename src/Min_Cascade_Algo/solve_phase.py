from representation import graph, random_phase
from algos import cascade_calculation
from pathlib import Path
import sys
import time
import file_manager
import numpy as np
import matplotlib.pyplot as plt

import cProfile

import pulp

mode_list = ["classic", "general", "intra_cluster_only", "perfect_build"]

choose_mode = sys.argv[1]
k = int(sys.argv[2])
l = int(sys.argv[3])
trial_number = int(sys.argv[4])
if choose_mode not in mode_list:
    raise ValueError("The mode that was entered does not exist. Existing modes: classic, general, intra_cluster_only")

def run():
    fm = file_manager.FileManager("best_examples")
    best_score = fm.get_or_create_file(k, l, choose_mode)

    scores = []
    moves = []
    cascade_repartition = np.zeros(int(np.log2(k)))
    for i in range(trial_number):
        tmp_cascade_repartition = np.zeros(int(np.log2(k)))
        t0 = time.time()
        p = random_phase.RandomPhase(k, l, choose_mode)
        p.start_phase()

        # TO COMPUTE THE MAX COST OF A PHASE
        if best_score < sum(p.cascade_costs):
            best_score = sum(p.cascade_costs)
            fm.redo_file(best_score, p.history)
            scores.clear()
            scores.append(p.cascade_costs)
            moves.clear()
            moves.append(p.g.get_moves())
        elif best_score == sum(p.cascade_costs):
            fm.update_file(p.history)
            scores.append(p.cascade_costs)
            moves.append(p.g.get_moves())

        # TO CHECK THE PROPERTY: after each cascade, cost <= l*s*log(s), where s is the number of revealed edges
        for j in range(0, len(p.cascade_costs)):
            if sum(p.cascade_costs[:j]) > l * (j + 1) * np.log2(j + 1):
                fm.store_counter_example("best_examples", "false lslog(s) property ", p.history, p.cascade_costs, j)
                print("counter example!! false lslog(s) property")
                break

        # TO CHECK THE PROPERTY: after each cascade, cost <= max(2, l*s*log(s)), where s is the number of revealed edges
        for j in range(0, len(p.cascade_costs)):
            if sum(p.cascade_costs[:j + 1]) > max(2, l * (j + 1) * np.log2(j + 1)):
                fm.store_counter_example("best_examples", "false max(2, lslog(s) property) ", p.history, p.cascade_costs, j)
                print("counter example!! false max(2, lslog(s) property")
                break

        # TO SEE THE REPARTITION OF CASCADES, DEPENDING ON THEIR COST
        for c in p.cascade_costs:
            index = int(np.log2(int(c/l)))
            tmp_cascade_repartition[index] += 1
        for j in range(len(tmp_cascade_repartition)):
            if tmp_cascade_repartition[j] > cascade_repartition[j]:
                cascade_repartition[j] = tmp_cascade_repartition[j]

        duration = time.time() - t0
        remaining_time = (trial_number - i) * duration
        hours = remaining_time // 3600
        minutes = (remaining_time - hours * 3600) // 60
        print(i * 100 / trial_number, "% rem. time:", int(hours), "h", int(minutes), "m score:", sum(p.cascade_costs),
            "best :", best_score)
        print("cas. repart.: ", cascade_repartition)

    print("best score : ", best_score)

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

# def f(x):
#     return 2 * x * np.log2(x)
#
#
# score = np.asarray([sum(scores[0][:i]) for i in range(len(scores[0]))])
# X = np.asarray(range(1, len(score) + 1))
# plt.plot(X, score)
# plt.plot(X, f(X))
# plt.show()

# moves = np.asarray(p.moves)
# sizes = np.asarray(p.sizes)
# for j in range(len(moves)):
#     moves[j] = np.asarray(moves[j])
#     sizes[j] = np.asarray(sizes[j])
#
# width = 0.3
# np_step = len(moves[0])
#
# np.transpose(moves)
# np.transpose(sizes)
#
# # s = np.sum(sizes, axis=1)
# # mov = np.sum(moves, axis=1)
#
# for j in range(0, len(moves)):
#     for n in range(len(moves[j])):
#         if l * np.log2(k) * sizes[j, n] < moves[j, n]:
#             print("False !!")
#             for h in p.history:
#                 print(h)
#         elif sizes[j, n] > 0:
#             if moves[j, n] / (l * np.log2(k) * sizes[j, n]) > seuil:
#                 print("diff = ", moves[j, n] / (l * np.log2(k) * sizes[j, n]))


# for j in range(0, len(moves)):
#     if l * np.log2(s[j]) * s[j] < mov[j]:
#         print("False !!")
#         for h in p.history:
#             print(h)
#     elif s[j] > 0:
#         if mov[j] / (l * np.log2(s[j]) * s[j]) > seuil:
#             print("diff = ", mov[j] / (l * np.log2(s[j]) * s[j]))
# print("rest = ", trial_number - i)

# plt.bar(range(len(moves)), [sum(moves[i]) for i in range(len(moves))], width=width, color='r')
# plt.bar(range(len(sizes)), np.log2(k) * np.sum(sizes, axis=1), alpha=0.5, width=width,
#         color='g')
#
# for i in range(1, len(moves)+1):
#     #bins = [x + 0.5 for x in range(0, len(moves[:][i-1]))]
#     plt.subplot(l, k, i)
#     # plt.plot(moves[i-1])
#     # plt.plot(2 * np.log2(k) * np.asarray(sizes[i-1]))
#     plt.bar(range(len(moves[i-1])), moves[i-1], width=width, color='r')
#     plt.bar(range(len(sizes[i-1])), np.log2(k) * np.asarray(sizes[i-1]), alpha=0.5, width=width, color='g')
#
# plt.legend(['cumulative costs', 'l.one_step_cost.log2(k)'], loc=4)
# plt.show()
