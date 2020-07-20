from representation import component, graph, counter


class Cluster:

    # default constructor with all components sizes at 1
    def __init__(self, k, id, g):
        self.g = g
        self.comp_list = []
        self.id = id
        self.k = k
        for i in range(k):
            self.comp_list.append(component.Component(1, counter.Counter.get_component_id()))

    def __init__(self, k, id, size_string, g):
        size_list = size_string.split(" ")
        self.g = g
        self.comp_list = []
        self.id = id
        self.k = k

        tmp_counter = 0
        for i in range(len(size_list)):
            comp_id = counter.Counter.get_component_id()
            if g.merge_char in size_list[i]:
                g.add_comp_to_merge(comp_id)
                size_list[i] = size_list[i].replace(g.merge_char, "")
            self.comp_list.append(component.Component(int(size_list[i]), comp_id))
            tmp_counter += int(size_list[i])

        if k != tmp_counter:
            print("Cluster n ", id, " was initialized with wrong components sizes")
            return


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
        tmp = tmp[:len(tmp)-1]
        return tmp

    def to_beautiful_string(self, thickness):
        tmp_string = ""
        for i in range(len(self.comp_list)):
            tmp_string += self.comp_list[i].to_beautiful_string(thickness) + '\n'
        tmp_string = tmp_string[:len(tmp_string) - 1]
        return tmp_string