import random


class CoinGame:
    def __init__(self, bet):
        self._result = False
        self.flip_coin()

    # x3
    def take_money(self):
        pass
    # x2

    def give_money(self):
        pass

    def flip_coin(self):
        possible_results = [True, False]
        self._result = random.choice(possible_results)



