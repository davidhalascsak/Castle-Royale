class Player:

    def __init__(self, name):
        self._name = name
        self._gold = 0
        self._structures = []
        self.state = None

    def calculate_gold_bonus(self):
        sum = 0
        for _ in self._structures:
            sum += 10
        return sum

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, change):
        self._gold = change

    @property
    def name(self):
        return self._name

