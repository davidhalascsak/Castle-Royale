import pickle
from os import walk


class Persistence:
    def __init__(self):
        self.saves = None

    def load_saves(self):
        self.saves = next(walk("saves"), (None, None, []))[2]
        # print(self.saves)

    def load(self, nr):
        self.load_saves()
        if len(self.saves) > 0 and 0 <= nr < len(self.saves):
            input = open("saves/{}.map".format(nr), "rb")
            obj = pickle.load(input)
            input.close()
            return obj
        return None

    def save(self, game_obj):
        if game_obj:
            self.load_saves()
            new_nr = len(self.saves)

            out = open("saves/{}.map".format(new_nr), "wb")
            pickle.dump(game_obj, out)
            out.close()

            self.load_saves()

    def get_num_saves(self):
        self.load_saves()
        return len(self.saves)


# obj = {1, 2, 3, 4, 5}
# p = Persistence()
# p.save(obj)

# print(p.load(1))
