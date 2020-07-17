import pulp as p
import numpy as np


class Calculation:

    # G is the graph, id1 and id2 are the two component ids to be merged
    @classmethod
    def possible_cascade(cls, g):
        k = g.k
        l = g.l
        id1, id2 = g.comps_to_merge[0], g.comps_to_merge[1]
        Lp_prob = p.LpProblem('cascade', p.LpMinimize)
        belonging_array, sizes, ids, index1, index2 = g.belonging_array(id1, id2)
        m = len(sizes)

        # creating the variables
        xs = [p.LpVariable("x{0}_{1}".format(i, j), cat="Binary")
              for i in range(m) for j in range(l)]
        xs = np.array(xs)
        xs = xs.reshape((m, l))

        # minimize objective
        objective = p.lpSum([sizes[i] * xs[i, j] * belonging_array[i, j]] for i in range(m) for j in range(l))
        Lp_prob += objective

        # conditions
        # conditions for respecting the sizes of components
        for i in range(l):
            Lp_prob += p.lpSum([sizes[j] * xs[j, i]] for j in range(m)) == k
        # conditions to make sure that any component is in one cluster at the time
        for i in range(m):
            Lp_prob += p.lpSum([xs[i, j]] for j in range(l)) == 1
        # condition to make sure that the two compnents that must merge will be in the same cluster
        for i in range(l):
            Lp_prob += xs[index1, i] == xs[index2, i]
        # solving the problem
        Lp_prob.solve()

        # Comunicating the results to create a new graph
        if Lp_prob.sol_status != 1:
            print("No feasible solution")
            return "", -1
        else:

            size_merged_comp = sizes[index1] + sizes[index2]
            is_merged_comp_treated = False
            new_graph = ""
            for i in range(l):
                for j in range(m):
                    if int(sizes[j] * xs[j, i].varValue) != 0:
                        if j == index1 or j == index2:
                            if not is_merged_comp_treated:
                                is_merged_comp_treated = True
                                new_graph += str(int(size_merged_comp * xs[j, i].varValue)) + " "
                        else:
                            new_graph += str(int(sizes[j] * xs[j, i].varValue)) + " "
                new_graph = new_graph[:len(new_graph) - 1]
                new_graph += '\n'
            new_graph = new_graph[:len(new_graph) - 1]
            return new_graph, p.value(Lp_prob.objective)
