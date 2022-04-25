import sqlite3


class Wallet:
    def __init__(self, player, start_balance):
        self._balance = start_balance
        self._player = player

    def add_money(self, money_amount):
        self._balance += money_amount

    def take_money(self, money_amount):
        if money_amount <= self._balance:
            self._balance -= money_amount

    def get_balance(self):
        return self._balance

    def __eq__(self, other):
        return other == self._player

    def __repr__(self):
        return self._player
