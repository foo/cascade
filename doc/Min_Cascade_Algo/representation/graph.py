from representation import cluster, counter
import numpy as np


class Graph:

    def __init__(self, k, l):
        self.k = k
        self.l = l
        self.cluster_list = []

        counter.Counter.reset()
        for i in range(self.l):
            self.cluster_list.append(cluster.Cluster(self.k, i))

    def __init__(self, graph_address):
        file_object = open(graph_address, 'r')
        self.k = int(file_object.readline())
        self.l = int(file_object.readline())
        self.cluster_list = []

        counter.Counter.reset()
        for i in range(self.l):
            tmp = file_object.readline()
            self.cluster_list.append(cluster.Cluster(self.k, i, list(map(int, tmp.split(" ")))))

    # new_graph is a string representation of the graph
    def actualisation(self, new_graph):
        new_graph_split = new_graph.split('\n')
        if int(new_graph_split[0]) != self.k or int(new_graph_split[1]) != self.l:
            print("k or l values are not as expected")
        else:
            counter.Counter.reset()
            for i in range(len(self.cluster_list)):
                self.cluster_list[i].actualisation(new_graph_split[i + 2])

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
        tmp = str(self.k) + "\n"
        tmp += str(self.l) + "\n"
        for c in self.cluster_list:
            tmp += c.to_string() + "\n"
        return tmp

    def comp_number(self):
        tmp = 0
        for c in self.cluster_list:
            tmp += c.comp_number()
        return tmp

    # def saturation(self, ):