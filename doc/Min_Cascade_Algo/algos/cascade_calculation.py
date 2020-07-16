import pulp as p
import numpy as np


class Calculation:

    #G is the graph, id1 and id2 are the two component ids to be merged
    @classmethod
    def possible_cascade(cls, g, id1, id2):
        k = g.k
        l = g.l
        Lp_prob = p.LpProblem('cascade', p.LpMinimize)

        belonging_array, sizes, ids, index1, index2 = g.belonging_array(id1, id2)
        index_merge = min(index1, index2)
        index_not_merge = max(index1, index2)
        m = len(sizes)

        tmp_list = list(range(m))
        del tmp_list[index_not_merge]
        del tmp_list[index_merge]
        xs = [p.LpVariable("x{0}_{1}".format(i, j), cat="Binary")
              for i in tmp_list for j in range(l)]
        xs += [p.LpVariable("x_move_{0}".format(i), cat='Binary') for i in range(l)]
        xs = np.array(xs)
        xs = xs.reshape((m-1, l))


        # minimize objective

        reduced_sizes = sizes.copy()
        reduced_sizes.append(reduced_sizes[index_merge] + reduced_sizes[index_not_merge])
        del reduced_sizes[index_not_merge]
        del reduced_sizes[index_merge]
        reduced_belonging_array = np.delete(belonging_array, [index_merge, index_not_merge], 0)

        objective = p.lpSum([])
        objective += p.lpSum([reduced_sizes[i] * xs[i, j] * reduced_belonging_array[i, j]] for i in range(m-2) for j in range(l))
        objective += p.lpSum([sizes[index_merge] * xs[-1, j] * belonging_array[index_merge, j]] for j in range(l))
        objective += p.lpSum([sizes[index_not_merge] * xs[-1, j] * belonging_array[index_not_merge, j]] for j in range(l))
        Lp_prob += objective

        # conditions
        # conditions for respecting the sizes of components
        for i in range(l):
            cond = p.lpSum([reduced_sizes[j] * xs[j, i]] for j in range(m-1))
            Lp_prob += cond == k
        # conditions to make sure that any component is in one cluster at the time
        for i in range(m-1):
            cond = p.lpSum([xs[i, j]] for j in range(l))
            Lp_prob += cond == 1

        # solving the problem
        Lp_prob.solve()

        # Comunicating the results to create a new graph
        if Lp_prob.sol_status != 1:
            print("No feasible solution")
            return ""
        else:

            new_graph = str(k) + "\n" + str(l)
            for i in range(l):
                new_graph += "\n"
                for j in range(m-1):
                    if int(reduced_sizes[j] * xs[j,i].varValue) != 0:
                        new_graph += str(int(reduced_sizes[j] * xs[j,i].varValue)) + " "
                new_graph = new_graph[:len(new_graph)-1]
                    #new_graph += str(int(Lp_prob.variables()[j * l + i].varValue)) + " "
            return new_graph, p.value(Lp_prob.objective)















        