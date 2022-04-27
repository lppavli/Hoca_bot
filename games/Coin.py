import random
import time


class CoinGame:
    def __init__(self, bet):
        self._result = False
        self._bet = int(bet)
        self._coefficients = {'win': 2, 'loss': 3}
        self.flip_coin()

    def determine_balance_after_flip(self):
        if self._result:
            return self._bet // self._coefficients["win"]
        else:
            return self._bet // self._coefficients['loss'] * 2

    def flip_coin(self):
        possible_results = [True, False]
        self._result = random.choice(possible_results)

    def get_result(self):
        return self._result
