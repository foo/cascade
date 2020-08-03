import matplotlib.pyplot as plt
import numpy as np

def intra_cluster_cost(k, l):
    if k <= 1:
        return 0
    else:
        return l * 2 * (k // 2) + intra_cluster_cost(k // 2, l) + intra_cluster_cost(k // 2 + k % 2, l)


l = 2
for i in range(1, 100):
    print(i, " : ", intra_cluster_cost(i, l), "    log : ", l * i * np.log2(i))

# X = range(1, 101)
# Y = [intra_cluster_cost(k, 1) for k in X]
#
# plt.plot(X, Y)
# plt.show()
