def cycle(seq):
    full = list(seq)
    while True:
        for i in full:
            yield i


class Game:
    def __init__(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.turns = cycle('OX')
        self._switch_player()
        self.game_over = False

    def _switch_player(self):
        self.current_player = next(self.turns)

    def _has_winner(self):
        def is_equal_row(row):
            return all(row) and len(set(row)) == 1

        inverted_board = [
            [line[0] for line in self.board],
            [line[1] for line in self.board],
            [line[2] for line in self.board],
        ]
        return any([
            any(is_equal_row(line) for line in self.board),
            any(is_equal_row(line) for line in inverted_board),
            is_equal_row([self.board[0][0], self.board[1][1], self.board[2][2]]),
            is_equal_row([self.board[2][0], self.board[1][1], self.board[0][2]])
        ])

    def _is_full(self):
        return all(all(line) for line in self.board)

    def play(self, row, column):
        # XXX: using KeyError because of VOC#352
        if self.game_over or self.board[row][column]:
            raise KeyError("Invalid play")
        self.board[row][column] = self.current_player
        if self._has_winner():
            self.game_over = True
            raise KeyError("Winner: " + self.current_player)
        elif self._is_full():
            self.game_over = True
            raise KeyError("Tie!")
        self._switch_player()

    def print(self):
        for line in self.board:
            print(' '.join(line))
