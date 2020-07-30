from representation import cluster, counter, cascade_changes
import numpy as np
import random as rd


class Graph:

    def __init__(self, k, l):
        self.k = k
        self.l = l
        self.comps_to_merge = []
        self.cluster_list = []
        self.merge_char = '*'
        self.power_char = '^'

        counter.Counter.reset()
        for i in range(l):
            self.cluster_list.append(cluster.Cluster(self.k, i, self))

    # def __init__(self, graph_string):
    #
    #     self.comps_to_merge = []
    #     self.merge_char = '*'
    #     self.power_char = '^'
    #
    #     graph_lines = self.transcription(graph_string)
    #
    #     print(graph_lines)
    #
    #     self.k = sum(list(map(int, graph_lines[0].replace(self.merge_char, "").split(" "))))
    #     self.l = len(graph_string.split("\n"))
    #     self.cluster_list = []
    #
    #     counter.Counter.reset()
    #     for i in range(self.l):
    #         self.cluster_list.append(cluster.Cluster(self.k, i, graph_lines[i], self))

    def next_request(self, choose_mod):
        if choose_mod == "random":
            comp_id_list = self.get_id_list()
            # if len(comp_id_list) <=1 or len(comp_id_list[0])<=1:
            #     print("too few components")
            #     return
            tmp1 = rd.choice(comp_id_list)
            comp1 = rd.choice(tmp1)
            comp_id_list.remove(tmp1)
            tmp2 = rd.choice(comp_id_list)
            comp2 = rd.choice(tmp2)
            return [comp1, comp2]

        #random requests, even btw comps in the same cluster
        if choose_mod == "total_random":
            comp_id_list = self.get_all_ids_in_one_list()
            # if len(comp_id_list) <=1 or len(comp_id_list[0])<=1:
            #     print("too few components")
            #     return
            comp1 = rd.choice(comp_id_list)
            comp_id_list.remove(comp1)
            comp2 = rd.choice(comp_id_list)
            return [comp1, comp2]

        if choose_mod == "intra_cluster_only":
            comp_id_list = self.get_id_list()
            while len(comp_id_list) > 0:
                tmp1 = rd.choice(comp_id_list)
                comp1 = rd.choice(tmp1)
                tmp1.remove(comp1)
                if len(tmp1) > 0:
                    comp2 = rd.choice(tmp1)
                    return [comp1, comp2]
                else:
                    comp_id_list.remove(tmp1)

            return [self.get_id_list()[0][0], self.get_id_list()[1][0]]

        if choose_mod == "smallest equal":
            # the components in each clusters are supposed to be sorted
            smallest_comp_list = []
            for c in self.cluster_list:
                c.reset_comp_counter()
                smallest_comp_list.append(c.next_comp())

            if len(smallest_comp_list) < 2:
                print("Only one cluster in Graph.next_request, choose_mod = smallest equal")
            tmp_counter = self.comp_number()
            while tmp_counter > 0:
                sorted_comps = sorted(smallest_comp_list, key=lambda tup: tup[1])
                smallest_comp = sorted_comps[0][1]
                if sorted_comps[0][1] == sorted_comps[1][1]:
                    return [sorted_comps[0][0], sorted_comps[1][0]]
                else:
                    for i in range(len(smallest_comp_list)):
                        if smallest_comp_list[i][1] == smallest_comp:
                            smallest_comp_list[i] = self.cluster_list[i].next_comp()
                            break
                tmp_counter -= 1

            smallest_comp_list = []
            for c in self.cluster_list:
                c.reset_comp_counter()
                smallest_comp_list.append(c.next_comp())
            sorted_comps = sorted(smallest_comp_list, key=lambda tup: tup[1])
            return [sorted_comps[0][0], sorted_comps[1][0]]

    def two_smallest_identic(self):
        smallest_comp_list = []
        for c in self.cluster_list:
            c.reset_comp_counter()
            smallest_comp_list.append(c.next_comp())

        if len(smallest_comp_list) < 2:
            print("Only one cluster in Graph.next_request, choose_mod = smallest equal")
        tmp_counter = self.comp_number()
        while tmp_counter > 0:
            sorted_comps = sorted(smallest_comp_list, key=lambda tup: tup[1])
            smallest_comp = sorted_comps[0][1]
            if sorted_comps[0][1] == sorted_comps[1][1]:
                return [sorted_comps[0][0], sorted_comps[1][0]]
            else:
                for i in range(len(smallest_comp_list)):
                    if smallest_comp_list[i][1] == smallest_comp:
                        smallest_comp_list[i] = self.cluster_list[i].next_comp()
                        break
            tmp_counter -= 1

        smallest_comp_list = []
        for c in self.cluster_list:
            c.reset_comp_counter()
            smallest_comp_list.append(c.next_comp())
        sorted_comps = sorted(smallest_comp_list, key=lambda tup: tup[1])
        return [sorted_comps[0][0], sorted_comps[1][0]]

    # new version of actualisation : the graph receives the exchanges the comps should do, and it exchange them instead of recreating them from scratch
    def apply_cascade(self, graph_changes):
        id_move1 = graph_changes.id_move1
        id_move2 = graph_changes.id_move2
        exchange_list = graph_changes.exchange_list

        for c in self.cluster_list:
            c.reset_reserve()

        for ex in exchange_list:
            i1 = ex[0]
            i2 = ex[1]
            id = ex[2]
            comp = self.cluster_list[i1].get_and_delete_comp(id)
            self.cluster_list[i2].add_to_reserve(comp)

        for c in self.cluster_list:
            c.remove_gone_comps()

        for c in self.cluster_list:
            c.apply_cascade(id_move1, id_move2)

    def get_cluster(self, id):
        for c in self.cluster_list:
            if c.id == id:
                return c
        return None

    # return a list of binaries, that describes where is located every component
    def belonging_array(self, id1, id2):
        m = self.comp_number()
        belonging_array = np.ones((m, self.l))
        id_array = np.zeros((m, self.l))
        sizes = []
        counter = 0
        for i in range(self.l):
            sizes += self.cluster_list[i].get_sizes()
            tmp_ids_list = self.cluster_list[i].get_ids()
            if id1 in tmp_ids_list:
                index1 = counter + tmp_ids_list.index(id1)
            if id2 in tmp_ids_list:
                index2 = counter + tmp_ids_list.index(id2)

            m = self.cluster_list[i].comp_number()
            id_array[counter:counter + m, i] = np.asarray(tmp_ids_list)  # DOUBTFULL

            for j in range(m):
                belonging_array[counter, i] = 0
                counter += 1
        return belonging_array, sizes, id_array, index1, index2

    def belonging_array_v2(self, id1, id2):
        m = self.comp_number()
        belonging_array = np.ones((m, self.l))
        id_array = np.zeros((m, self.l))
        sizes = np.zeros((m, self.l))
        comp_sizes = []
        counter = 0

        # Initialisation of sizes
        for cl in self.cluster_list:
            for comp in cl.comp_list:
                for id in comp.cluster_id:
                    sizes[counter, id] += 1
                counter += 1

        counter = 0
        for i in range(self.l):
            comp_sizes += self.cluster_list[i].get_sizes()
            tmp_ids_list = self.cluster_list[i].get_ids()
            if id1 in tmp_ids_list:
                index1 = counter + tmp_ids_list.index(id1)
            if id2 in tmp_ids_list:
                index2 = counter + tmp_ids_list.index(id2)

            m = self.cluster_list[i].comp_number()
            id_array[counter:counter + m, i] = np.asarray(tmp_ids_list)  # DOUBTFULL

            for j in range(m):
                belonging_array[counter, i] = 0
                counter += 1
        return belonging_array, sizes, comp_sizes, id_array, index1, index2

    def to_string(self, next_request=None):
        if next_request is not None:
            tmp = ""
            for c in self.cluster_list:
                tmp += c.to_string(next_request, self.merge_char) + "\n"
            return tmp
        else:
            tmp = ""
            for c in self.cluster_list:
                tmp += c.to_string() + "\n"
            return tmp

    def to_beautiful_string(self, thickness=5, gap_btw_clusters=2):
        tmp_string = ""
        tmp_array = []
        for i in range(len(self.cluster_list)):
            tmp_cluster_array = self.cluster_list[i].to_beautiful_string(thickness).split("\n")
            if len(tmp_cluster_array) != self.k:
                print("Error in the size of a cluster in his beautiful string representation")
                return
            tmp_array.append(tmp_cluster_array)
        tmp_array = np.transpose(np.asarray(tmp_array))
        for i in range(len(tmp_array)):
            for j in range(len(tmp_array[i])):
                tmp_string += " " * gap_btw_clusters + tmp_array[i, j]
            tmp_string += '\n'
        return tmp_string

    def transcription(self, graph_string):

        lines = graph_string.split("\n")
        for i in range(len(lines)):
            line_split = lines[i].split(" ")
            for j in range(len(line_split)):
                is_merge_char = False
                if self.merge_char in line_split[j]:
                    line_split[j] = line_split[j].replace(self.merge_char, "")
                    is_merge_char = True

                if self.power_char in line_split[j]:
                    tmp = line_split[j].split(self.power_char)
                    if len(tmp) != 2:
                        print("Bad format concerning power char : ", self.power_char)
                        return
                    new_string = ""
                    for m in range(int(tmp[1])):
                        new_string += tmp[0] + " "
                    new_string = new_string[:len(new_string) - 1]
                    line_split[j] = new_string
                if is_merge_char:
                    line_split[j] += self.merge_char
            lines[i] = " ".join(line_split)
        return lines

    def get_last_cascade_cost(self):
        last_cascade_cost = 0
        for c in self.cluster_list:
            last_cascade_cost += c.get_last_cascade_cost()
        return last_cascade_cost

    def add_comp_to_merge(self, comp_id):
        if len(self.comps_to_merge) >= 2:
            print("More than two components to be merged are indicated. Only the first two are taken in account")
            return
        self.comps_to_merge.append(comp_id)

    def comp_number(self):
        tmp = 0
        for c in self.cluster_list:
            tmp += c.comp_number()
        return tmp

    def get_last_move(self):
        tmp = []
        for c in self.cluster_list:
            tmp += c.get_last_move()
        return tmp

    def get_moves(self):
        tmp = []
        for c in self.cluster_list:
            tmp += c.get_moves()
        return tmp

    def get_all_ids_in_one_list(self):
        tmp = []
        for c in self.cluster_list:
            tmp += c.get_ids()
        return tmp

    def get_id_list(self):
        tmp = []
        for c in self.cluster_list:
            tmp.append(c.get_ids())
        return tmp

    def get_comp(self, id):
        for c in self.cluster_list:
            tmp = c.get_comp(id)
            if tmp is not None:
                return tmp
        return None


    def get_sizes(self):
        tmp = []
        for c in self.cluster_list:
            tmp += c.get_sizes()
        return tmp

    def get_sizes_per_clusters(self):
        tmp = []
        for c in self.cluster_list:
            tmp.append(c.get_sizes())
        return tmp

    # def saturation(self, ):
