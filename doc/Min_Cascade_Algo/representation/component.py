from representation import node


class Component:

    def __init__(self, size, id):
        #self.node_list = [node.Node(id)]
        self.size = size
        self.id = id

    def to_string(self):
        return str(self.size)



