from representation import graph, phase
from algos import cascade_calculation
from pathlib import Path
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import os.path
from pathlib import Path

def rename_file(best_score, output_file):
    split = output_file.split(" ")
    del split[-1]
    split.append("bs=" + str(best_score) + ".txt")
    tmp = ""
    for s in split:
        tmp += s + " "
    tmp = tmp[:len(tmp)-1]
    return tmp


mode_list = ["classic", "general", "intra_cluster_only"]

choose_mode = sys.argv[1]
k = int(sys.argv[2])
l = int(sys.argv[3])
trial_number = int(sys.argv[4])
output_file = "best_examples"

if choose_mode not in mode_list:
    raise ValueError("The mode that was entered does not exist. Existing modes: classic, general, intra_cluster_only")
if not os.path.exists(output_file + "/" + str(choose_mode)):
    Path(output_file + "/" + str(choose_mode)).mkdir(parents=True, exist_ok=True)
output_file = output_file + "/" + str(choose_mode)
if not os.path.exists(output_file + "/" + choose_mode + " l=" + str(l)):
    Path(output_file + "/" + choose_mode + " l=" + str(l)).mkdir(parents=True, exist_ok=True)
output_file += "/" + choose_mode + " l=" + str(l)
if len([filename for filename in os.listdir(output_file) if filename.startswith(choose_mode + " l=" + str(l) + " k=" + str(k))]) == 0:
    output_file += "/" + choose_mode + " l=" + str(l) + " k=" + str(k) + " bs=0.txt"
    my_file = open(output_file, "w+")
    best_score = 0
else:
    file_name = [filename for filename in os.listdir(output_file) if filename.startswith(choose_mode + " l=" + str(l) + " k=" + str(k))][0]
    best_score = int(file_name.split(" ")[-1].split(".")[0][3:])
    output_file += "/" + file_name
    my_file = open(output_file, "w+")

scores = []
moves = []
for i in range(trial_number):
    t0 = time.time()
    p = phase.Phase(k, l, choose_mode)
    p.start_phase()
    if best_score < sum(p.cascade_costs):
        best_score = sum(p.cascade_costs)
        my_file.close()
        os.rename(output_file, rename_file(best_score, output_file))
        output_file = rename_file(best_score, output_file)
        my_file = open(output_file, "w+")
        my_file.truncate(0)
        my_file.write("\n\n\n")
        my_file.write(p.history)
        scores.clear()
        scores.append(p.cascade_costs)
        moves.clear()
        moves.append(p.g.get_moves())
    elif best_score == sum(p.cascade_costs):
        my_file.write("\n\n\n")
        my_file.write(p.history)
        scores.append(p.cascade_costs)
        moves.append(p.g.get_moves())
    duration = time.time() - t0
    remaining_time = (trial_number - i) * duration
    hours = remaining_time // 3600
    minutes = (remaining_time - hours * 3600) // 60
    print(i * 100 / trial_number, "%   rem. time: ", int(hours), "h", int(minutes), "m   best : ", best_score)

print("best score : ", best_score)




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
