import random


class RockPaperScissorsGame:
    def __init__(self, player1, player2, guild):
        self._player1 = player1
        self._player2 = player2
        self.guild = guild
        self.choices = {self._player1: False, self._player2: False}
        self.not_winner = ''

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
                elif player2_choice == i and player1_choice == j:
                    result = self._player2

        return 'Победил ' + result

    def can_show_result(self, request_guild):
        if self.choices[self._player1] and self.choices[self._player2]:
            if request_guild == self.guild:
                return True

    def show_result(self):
        player1_choice = self.choices[self._player1]
        player2_choice = self.choices[self._player2]

        result = self.find_winner(player1_choice, player2_choice)

        return f"{result}, выбор игроков:\n" \
               f"{self._player1} - {self.choices[self._player1]}\n" \
               f"{self._player2} - {self.choices[self._player2]}"

    def __eq__(self, other):
        return other in self.choices

    def __repr__(self):
        return str(self.choices)

    def get_players(self):
        return self._player1, self._player2
