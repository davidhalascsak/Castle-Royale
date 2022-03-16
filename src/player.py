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

    def get_gold_bonus(self):
        sum_gold = 0
        for _ in self.structures:
            sum_gold += 10
        return sum_gold

