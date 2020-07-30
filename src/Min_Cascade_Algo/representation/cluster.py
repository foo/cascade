from representation import component, graph, counter


class Cluster:

    # default constructor with all components sizes at 1
    def __init__(self, k, id, g):
        self.g = g
        self.comp_list = []
        self.id = id
        self.ids_to_delete = []
        self.k = k
        self.comp_reserve = []
        self.comp_counter = 0
        for i in range(k):
            self.comp_list.append(component.Component(1, counter.Counter.get_component_id(), self.id))

    # def __init__(self, k, id, size_string, g):
    #     size_list = size_string.split(" ")
    #     self.g = g
    #     self.comp_list = []
    #     self.id = id
    #     self.k = k
    #     self.comp_reserve = []
    #     self.ids_to_delete = []
    #
    #     tmp_counter = 0
    #     for i in range(len(size_list)):
    #         comp_id = counter.Counter.get_component_id()
    #         if g.merge_char in size_list[i]:
    #             g.add_comp_to_merge(comp_id)
    #             size_list[i] = size_list[i].replace(g.merge_char, "")
    #         self.comp_list.append(component.Component(int(size_list[i]), comp_id))
    #         tmp_counter += int(size_list[i])
    #
    #     if k != tmp_counter:
    #         print("Cluster n ", id, " was initialized with wrong components sizes")
    #         return
    #
    #     self.comp_list = sorted(self.comp_list, key=lambda comp: comp.size)

    def remove_gone_comps(self):
        i = 0
        while i < len(self.comp_list):
            if self.comp_list[i].id in self.ids_to_delete:
                del self.comp_list[i]
            else:
                i += 1

    def apply_cascade(self, id_move1, id_move2):
        for c in self.comp_list:
            c.did_not_move()
            if id_move1 in self.get_ids() and id_move2 in self.get_ids():
                comp1 = self.get_comp(id_move1)
                comp2 = self.get_comp(id_move2)
                comp1.moves += 2 * min(comp1.size, comp2.size)
                comp1.last_move = 2 * min(comp1.size, comp2.size)
        for c in self.comp_reserve:
            self.comp_list.append(c)
            c.move()
        comp1 = self.get_comp(id_move1)
        comp2 = self.get_comp(id_move2)

        if (comp1 is not None and comp2 is None) or (comp1 is None and comp2 is not None):
            print("Found one component to merge in cluster ", self.id, ", but not the other")
        elif comp1 is not None and comp2 is not None:
            comp1.merge(comp2)
            self.comp_list.remove(comp2)

        if sum(self.get_sizes()) != self.k:
            print("Size error in cluster ", self.id, " during apply_cascade")

        self.comp_list = sorted(self.comp_list, key=lambda comp: comp.size)

    def add_to_reserve(self, comp):
        self.comp_reserve.append(comp)

    def get_last_cascade_cost(self):
        last_cascade_cost = 0
        for c in self.comp_list:
            last_cascade_cost += c.last_move
        return last_cascade_cost

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

    def get_last_move(self):
        tmp = []
        for c in self.comp_list:
            tmp.append(c.last_move)
        return tmp

    def get_moves(self):
        tmp = []
        for c in self.comp_list:
            tmp.append(c.moves)
        return tmp

    def get_comp(self, id):
        for c in self.comp_list:
            if c.id == id:
                return c
        return None

    def get_and_delete_comp(self, id):
        for c in self.comp_list:
            if c.id == id:
                self.ids_to_delete.append(id)
                return c
        return None

    def comp_number(self):
        return len(self.comp_list)

    def next_comp(self):
        if self.comp_counter < len(self.comp_list):
            self.comp_counter += 1
        return [self.comp_list[self.comp_counter - 1].id, self.comp_list[self.comp_counter - 1].size]

    def reset_comp_counter(self):
        self.comp_counter = 0
        return

    def reset_reserve(self):
        self.comp_reserve.clear()
        self.ids_to_delete.clear()

    def to_string(self, next_request=None, merge_char=None):
        if next_request is not None and merge_char is not None:
            tmp = ""
            for c in self.comp_list:
                if merge_char in c.to_string(next_request, merge_char):
                    tmp += c.to_string(next_request, merge_char) + " "
                else:
                    tmp += c.to_string(next_request, merge_char) + "  "
            tmp = tmp[:len(tmp) - 1]
            return tmp
        else:
            tmp = ""
            for c in self.comp_list:
                tmp += c.to_string() + " "
            tmp = tmp[:len(tmp) - 1]
            return tmp

    def to_beautiful_string(self, thickness):
        tmp_string = ""
        for i in range(len(self.comp_list)):
            tmp_string += self.comp_list[i].to_beautiful_string(thickness) + '\n'
        tmp_string = tmp_string[:len(tmp_string) - 1]
        return tmp_string
