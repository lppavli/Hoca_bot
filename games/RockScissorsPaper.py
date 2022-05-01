import random


class RockPaperScissorsGame:
    def __init__(self, player1: str, player2: str, ctx, bet):
        self._player1 = player1
        self._player2 = player2
        self.ctx = ctx
        self._bet = int(bet)
        self.choices = {self._player1: False, self._player2: False}
        self._not_winner = ''
        self._winner = ''

    def choose(self, choice, player):
        if player in self.choices and not self.choices[player]:
            permitted_choices = ['камень', 'ножницы', 'бумага']
            if choice not in permitted_choices:
                choice = random.choice(permitted_choices)
            self.choices[player] = choice

    def find_winner(self, player1_choice, player2_choice):
        variants = {
            "камень": "ножницы",
            "ножницы": "бумага",
            "бумага": "камень"
        }
        result = ''

        if player1_choice == player2_choice:
            return "Ничья"
        else:
            for i, j in variants.items():
                if player1_choice == i and player2_choice == j:
                    result = self._player1
                    self._winner = self._player1
                    self._not_winner = self._player2
                elif player2_choice == i and player1_choice == j:
                    result = self._player2
                    self._winner = self._player2
                    self._not_winner = self._player1

        return 'Победил ' + result

    def execute_winner(self):
        return self._winner

    def execute_not_winner(self):
        return self._not_winner

    def execute_bet(self):
        return self._bet

    def execute_players_names(self):
        return str(self._player1[:]), str(self._player2[:])

    def check_choices(self):
        return self.choices[self._player1] != 0 and self.choices[self._player2] != 0

    def can_show_result(self) -> bool:
        return self.check_choices()

    def show_result(self):
        player1_choice = self.choices[self._player1]
        player2_choice = self.choices[self._player2]

        result = self.find_winner(player1_choice, player2_choice)

        return f"{result}, выбор игроков:\n" \
               f"{self._player1} - {self.choices[self._player1]}\n" \
               f"{self._player2} - {self.choices[self._player2]}", self.ctx

    def __eq__(self, other):
        return other in self.choices

    def __repr__(self):
        return str(self.choices)

    def get_players(self):
        return self._player1, self._player2
