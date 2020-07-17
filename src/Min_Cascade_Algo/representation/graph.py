from representation import cluster, counter
import numpy as np
import re

class Graph:

    def __init__(self, graph_address):

        self.comps_to_merged = []
        self.merge_char = '*'
        self.power_char = '^'

        file_object = open(graph_address, 'r+')
        graph_lines = self.transcription(file_object)

        self.k = sum(list(map(int, graph_lines[0].replace(self.merge_char, "").split(" "))))
        file_object.seek(0)
        self.l = len(open(graph_address).readlines())
        file_object.seek(0)
        self.cluster_list = []

        counter.Counter.reset()
        for i in range(self.l):
            self.cluster_list.append(cluster.Cluster(self.k, i, list(map(int, graph_lines[i].split(" ")))))

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

    def transcription(self, file_object):

        lines = file_object.read().split("\n")
        for i in range(len(lines)):
            line_split = lines[i].split(" ")
            for j in range(len(line_split)):
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
            lines[i] = " ".join(line_split)
        return lines



    def comp_number(self):
        tmp = 0
        for c in self.cluster_list:
            tmp += c.comp_number()
        return tmp

    # def saturation(self, ):
