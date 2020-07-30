import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------- TOTAL PHASE COST TESTS ---------------------------

# X = np.asarray([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 20, 23, 25, 30, 40, 50, 100])
# Y_resuts = np.array([2, 6, 10, 18, 22, 30, 38, 46, 52, 60, 70, 84, 88, 94, 117, 144, 170, 190, 246, 368, 492, 1172])
# Y_comparison = 2 * X * np.log2(X)
#
# X_3D = np.asarray([2, 3, 4, 5, 6, 7, 8, 9, 10])
# Y_resuts_3D = np.asarray([4, 12, 19, 29, 40, 50, 58, 69, 84])
# Y_comparison_3D = 3 * X_3D * np.log2(X_3D)
#
#
# plt.plot(X, Y_resuts, label='max phase cost (biggest cost among 500 random phases)')
# plt.plot(X, Y_comparison, label="l.k.log2(k)")
# plt.title("L = 2")
# plt.xlabel("cluster capacity")
# plt.ylabel("phase costs")
# plt.legend(['max phase cost (biggest cost among 500 random phases)', 'l.k.log2(k)'], loc=4)
# plt.show()

# ------------------------------------- STEP BY STEP PHASE COST TESTS ---------------------------
#
# x1 = [1, 2, 2, 3, 4, 4, 4, 4, 4, 5, 5]
# x2 = [1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 5, 5]
# bins = [x + 0.5 for x in range(0, 6)]
# plt.hist(x1, bins = bins, color = 'yellow',
#             edgecolor = 'red', hatch = '/', label = 'x1')
# plt.hist(x2, bins = bins, color = 'green', alpha = 0.5,
#             edgecolor = 'blue', hatch = '/', label = 'x2')
# plt.ylabel('valeurs')
# plt.xlabel('nombres')
# plt.title('superpose')
# plt.legend()
# plt.show()
#
