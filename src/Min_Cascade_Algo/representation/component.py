from representation import node


class Component:

    def __init__(self, size, id, cluster_id):
        self.size = size
        self.id = id
        self.moves = 0
        self.last_move = 0
        self.id_list = [id]
        self.cluster_id = [cluster_id]


    def move(self):
        self.moves += self.size
        self.last_move = self.size

    def did_not_move(self):
        self.last_move = 0

    def merge(self, comp):
        self.size += comp.size
        self.id = min(self.id, comp.id)
        self.moves += comp.moves
        self.last_move += comp.last_move

        self.id_list += comp.id_list
        self.cluster_id += comp.cluster_id


    def to_string(self, next_request=None, merge_char=None):
        if next_request is not None and merge_char is not None and self.id in next_request:
            return str(self.size) + merge_char
        return str(self.size)

    def to_beautiful_string(self, thickness):
        if self.size == 1:
            return "|" + "¯"*int(thickness/2) + "1" + "¯"*int(thickness/2) + "|"
        if self.size == 2:
            return "|" + "¯"*thickness + "|" + "\n" + "|" + "_"*int(thickness/2) + "2" + "_"*int(thickness/2) + "|"
        else:
            tmp_string = "|" + "¯"*thickness + "|"
            for i in range(1, self.size-1):
                if i == int(self.size/2):
                    length_size = len(str(self.size))
                    tmp_string += "\n" + "|" + " "*(int((thickness-length_size+1)/2)) + str(self.size) + " "*(int((thickness-length_size)/2)) + "|"
                else:
                    tmp_string += "\n" + "|" + " "*thickness + "|"
            tmp_string += "\n" + "|" + "_"*thickness + "|"
            return tmp_string






