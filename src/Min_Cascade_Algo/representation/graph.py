from representation import cluster, counter
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

        for i in range(l):
            self.cluster_list.append(cluster.Cluster(self.k, i, self))

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

        if choose_mod == "smallest equal":
            #the components in each clusters are supposed to be sorted
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

    # new_graph is a string representation of the graph
    def actualisation(self, new_graph):
        new_graph_split = new_graph.split('\n')
        l_new = len(new_graph_split)
        k_new = sum(list(map(int, new_graph_split[0].replace(self.merge_char, "").split(" "))))
        if k_new != self.k or l_new != self.l:
            print("k or l values are not as expected: no graph actualisation")
        else:
            counter.Counter.reset()
            for i in range(len(self.cluster_list)):
                self.cluster_list[i].actualisation(new_graph_split[i])
        self.comps_to_merge = []

    # return a list of binaries, that describes where is located every component
    def belonging_array(self, id1, id2):
        m = self.comp_number()
        belonging_array = np.ones((m, self.l))
        sizes = []
        ids = []
        counter = 0
        for i in range(self.l):
            sizes += self.cluster_list[i].get_sizes()
            tmp_ids_list = self.cluster_list[i].get_ids()
            if id1 in tmp_ids_list:
                index1 = counter + tmp_ids_list.index(id1)
            if id2 in tmp_ids_list:
                index2 = counter + tmp_ids_list.index(id2)
            ids += tmp_ids_list

            m = self.cluster_list[i].comp_number()
            for j in range(m):
                belonging_array[counter, i] = 0
                counter += 1
        return belonging_array, sizes, ids, index1, index2

    def to_string(self):
        tmp = ""
        for c in self.cluster_list:
            tmp += c.to_string() + "\n"
        return tmp

    def to_beautiful_string(self, thickness = 5, gap_btw_clusters = 2 ):
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
                tmp_string += " "*gap_btw_clusters + tmp_array[i, j]
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

    def get_id_list(self):
        tmp = []
        for c in self.cluster_list:
            tmp.append(c.get_ids())
        return tmp

    # def saturation(self, ):
