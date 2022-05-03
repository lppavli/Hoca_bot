WHITE = 1
BLACK = 2


class Pawn:
    def __init__(self, color):
        self.color = color
        self.is_queened = False

    def set_position(self, row, col):
        row = row
        self.col = col

    def char(self):
        return 'P'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False
        if not self.is_queened:
            # Пешка может ходить только по вертикали
            # "взятие на проходе" не реализовано
            if col != col1:
                return False

            # Пешка может сделать из начального положения ход на 2 клетки
            # вперёд, поэтому поместим индекс начального ряда в start_row.
            if self.color == WHITE:
                direction = 1
                start_row = 1
            else:
                direction = -1
                start_row = 6

            # ход на 1 клетку
            if row + direction == row1:
                return True

            # ход на 2 клетки из начального положения
            if row == start_row and row + 2 * direction == row1:
                return True
        else:
            # Невозможно сделать ход в клетку, которая не лежит в том же ряду
            # или столбце клеток.
            piece1 = board.get_piece(row1, col1)
            if not (piece1 is None) and piece1.get_color() == self.color:
                return False
            if row == row1 or col == col1:
                step = 1 if (row1 >= row) else -1
                for r in range(row + step, row1, step):
                    if not (board.get_piece(r, col) is None):
                        return False
                step = 1 if (col1 >= col) else -1
                for c in range(col + step, col1, step):
                    if not (board.get_piece(row, c) is None):
                        return False
                return True
            if row - col == row1 - col1:
                step = 1 if (row1 >= row) else -1
                c = col
                for r in range(row + step, row1, step):
                    c += step
                    if not (board.get_piece(r, c) is None):
                        return False
                return True
            if row + col == row1 + col1:
                step = 1 if (row1 >= row) else -1
                c = col
                for r in range(row + step, row1, step):
                    c -= step
                    if not (board.get_piece(r, c) is None):
                        return False
                return True
            return False

        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8