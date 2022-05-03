from .queen import Queen
from .rook import Rook
from .pawn import Pawn
from .knight import Knight
from .bishop import Bishop
from .king import King


WHITE = 1
BLACK = 2


def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    board_display = list()

    board_display.append('⠀⠀⠀⠀⠀⠀⠀+====+====+====+====+====+====+====+====+')
    for row in range(7, -1, -1):
        board_display.append('⠀⠀⠀⠀⠀' + str(row) + '    ')
        for col in range(8):
            board_display[-1] += '|=' + board.cell(row, col) + '='
        board_display[-1] += '|'
        board_display.append('⠀⠀⠀⠀⠀⠀⠀+====+====+====+====+====+====+====+====+')
    board_display[-1] += '⠀⠀⠀⠀⠀⠀⠀⠀'
    board_display.append('⠀⠀⠀⠀⠀⠀⠀⠀' + str(0) + '⠀⠀')
    for col in range(1, 8):
        board_display[-1] += str(col) + '⠀⠀'
    board_display.append('')
    return board_display


class Starter:
    def __init__(self):
        self.board = Board()
        self.colors = {WHITE: 'Белых', BLACK: 'Черных'}

    def start(self):
        while True:
            to_discord = []
            for i in print_board(self.board):
                to_discord.append(i)
            to_discord.append('Команды:')
            to_discord.append('⠀⠀⠀⠀exit                               -- выход')
            to_discord.append('⠀⠀⠀⠀move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
            to_discord.append('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀в клетку (row1, col1)')
            if self.board.current_player_color() == WHITE:
                to_discord.append('Ход белых:')
            else:
                to_discord.append('Ход черных:')
            return to_discord

    def move(self, command):
        to_discord = []
        if command == 'exit':
            return
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if self.board.move_piece(row, col, row1, col1):
            to_discord.append('Ход успешен')
            if self.board.find_winner():
                to_discord.append(f'Победа {self.colors[self.board.find_winner()]}')
                return
        else:
            to_discord.append('Координаты некорректы! Попробуйте другой ход!')
        return to_discord


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            None, Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)
        return True

    def find_winner(self):
        kings_alive = []
        for i in self.field:
            for j in i:
                if type(j) == King:
                    kings_alive.append(j)
        if len(kings_alive) == 2:
            return False
        elif type(kings_alive[0]) == King:
            return kings_alive[0].get_color()


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8
