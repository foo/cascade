from representation import graph

class Cascade_Changes:

    #id_move1 and id_move2 are the ids of the comps to be merged. exchange_list elements are like [i1, i2, id]
    #where i1 and i2 are departure and arrival clusters, id is the comp id.
    def __init__(self, id_move1, id_move2, exchange_list):
        self.id_move1 = id_move1
        self.id_move2 = id_move2
        self.exchange_list = exchange_list