from representation import node


class Component:

    def __init__(self, size, id):
        #self.node_list = [node.Node(id)]
        self.size = size
        self.id = id

    def to_string(self):
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






