from representation import graph

class Counter:

    id_counter = 0
    moves_counter = 0

    @classmethod
    def get_component_id(cls):
        cls.id_counter += 1
        return cls.id_counter - 1

    @classmethod
    def reset(cls):
        cls.id_counter = 0

    @classmethod
    def refresh_move_counter(cls, move_number, g, request):
        if move_number > cls.moves_counter:
            cls.g = g.copy()
