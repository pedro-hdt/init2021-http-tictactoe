class GameException(Exception):
    pass

class TicTacToe:

    def __init__(self, n):
        self.n = n
        self.board = [[ ' ' for _ in range(n) ]  for _ in range(n) ]
        self.status = 'X'
        self.over = False
        self.play_count = 0

    def __str__(self): 
        sep_line = f'\n{"-" * (2 * self.n - 1)}\n'
        return sep_line.join(['|'.join(row) for row in self.board])

    def play(self, x, y, symbol):
        if self.over:
            raise GameException('This game is over')
        if symbol != self.next_player():
            raise GameException('It is not your turn')
        if x < 0 or y < 0 or x > self.n or y > self.n:
            raise GameException('Invalid position')
        if self.board[x][y] != ' ':
            raise GameException('Position already taken')
        self.board[x][y] = self.status
        self.play_count += 1
        if self._check_win(self.status):
            self.status += ' won'
            self.over = True
            return
        if self.play_count == self.n**2:
            self.over = True
            self.status = 'Tie'
            return
        self.status = 'X' if self.status == 'O' else 'O'

    def next_player(self):
        return self.status

    def _win_indices(self):
        for r in range(self.n): # rows
            yield [(r, c) for c in range(self.n)]
        for c in range(self.n): # columns
            yield [(r, c) for r in range(self.n)]
        # diagonals
        # top left to bottom right
        yield [(i, i) for i in range(self.n)]
        # top right to bottom left
        yield [(i, self.n - 1 - i) for i in range(self.n)]


    def _check_win(self, player):
        for indices in self._win_indices():
            if all(self.board[r][c] == player for r, c in indices):
                return True
        return False
