class Player:
    def __init__(self, name):
        self.name = name
        self.gold = 0
        self.structures = []

    def set_gold(self, gold):
        self.gold = gold

    def get_gold(self):
        return self.gold

    def get_name(self):
        return self.name
