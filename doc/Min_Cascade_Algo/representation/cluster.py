from reprentation import component
from reprentation import counter


class Cluster:

    # default constructor with all components sizes at 1
    def __init__(self, k, id):
        self.comp_list = []
        self.id = id
        self.k = k
        for i in range(k):
            self.comp_list.append(component.Component(1, counter.Counter.get_component_id()))

    def __init__(self, k, id, size_list):
        self.comp_list = []
        self.id = id
        self.k = k
        if k != sum(size_list):
            print("Cluster n ", id, " was initialized with wrong components sizes")
            return
        for i in range(len(size_list)):
            self.comp_list.append(component.Component(size_list[i], counter.Counter.get_component_id()))


    def actualisation(self, new_cluster):
        self.comp_list.clear()
        tmp = list(map(int, new_cluster.split(" ")))
        for i in range(len(tmp)):
            self.comp_list.append(component.Component(tmp[i], counter.Counter.get_component_id()))


    def get_ids(self):
        tmp = []
        for c in self.comp_list:
            tmp.append(c.id)
        return tmp

    def get_sizes(self):
        tmp = []
        for c in self.comp_list:
            tmp.append(c.size)
        return tmp

    def comp_number(self):
        return len(self.comp_list)

    def to_string(self):
        tmp = ""
        for c in self.comp_list:
            tmp += c.to_string() + " "
        return tmp
