class Knight:
    def __init__(self, color):
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'N'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if 8 > row1 > -1 and 8 > col1 > -1:
            if abs(row - row1) == 2 and abs(col - col1) == 1:
                return True
            elif abs(row - row1) == 1 and abs(col - col1) == 2:
                return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)