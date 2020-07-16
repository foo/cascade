from representation import graph
import copy

class Counter:

    id_counter = 0

    @classmethod
    def get_component_id(cls):
        cls.id_counter += 1
        return cls.id_counter - 1

    @classmethod
    def reset(cls):
        cls.id_counter = 0

