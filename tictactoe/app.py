import android
from android.util import Log
from android.widget import LinearLayout
from android.widget import Button
from android.widget import TextView
from android.view import Gravity
import android.view


# XXX: had to paste the game logic here, because importing was failing
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


def enumerate1(iterable):
    index = 0
    for it in iterable:
        yield (index, it)
        index += 1


def enumerate2(iterable):
    index = 0
    for it in iterable:
        yield (index, it)
        index += 1


class ButtonClick(implements=android.view.View[OnClickListener]):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def onClick(self, view: android.view.View) -> void:
        self.callback(*self.args, **self.kwargs)


class MyApp:
    def __init__(self):
        self._activity = None
        self.buttons = []
        self.top_label = None
        self.game = Game()
        self.message = None

    def link(self, activity):
        self._activity = activity

    def onCreate(self):
        def create_button_row():
            return [
                Button(self._activity),
                Button(self._activity),
                Button(self._activity),
            ]

        self.buttons = [
            create_button_row(),
            create_button_row(),
            create_button_row(),
        ]

        vlayout = LinearLayout(self._activity)
        vlayout.setOrientation(LinearLayout.VERTICAL)

        self.top_label = TextView(self._activity)
        self.top_label.setTextSize(50)
        vlayout.addView(self.top_label)

        for row in self.buttons:
            hlayout = LinearLayout(self._activity)
            hlayout.setOrientation(LinearLayout.HORIZONTAL)
            hlayout.setGravity(Gravity.CENTER)
            for button in row:
                button.setTextSize(50)
                hlayout.addView(button)

            vlayout.addView(hlayout)

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setOnClickListener(ButtonClick(self.play, i, j))

        self.restart_button = Button(self._activity)
        self.restart_button.setText('Restart')
        self.restart_button.setOnClickListener(ButtonClick(self.restart_game))
        vlayout.addView(self.restart_button)

        footer = TextView(self._activity)
        footer.setText('Powered by Python')
        footer.setGravity(Gravity.CENTER)
        vlayout.addView(footer)

        self.updateUI()

        self._activity.setContentView(vlayout)

    def restart_game(self):
        self.game = Game()
        self.message = None
        self.updateUI()

    def updateUI(self):
        if self.message:
            self.top_label.setText(self.message)
        else:
            self.top_label.setText('Player: ' + self.game.current_player)
        for i, row in enumerate1(self.buttons):
            for j, button in enumerate2(row):
                thing = self.game.board[i][j]
                if thing:
                    button.setText(thing)
                else:
                    button.setText(' ')

    def play(self, i, j):
        if self.game.game_over:
            return

        print('going to play game', self.game, ' in position:', i, j)
        try:
            self.game.play(i, j)
            self.message = None
        except KeyError as e:
            message = str(e)[1:-1]
            print('message', message)
            self.message = message
        self.updateUI()


app = MyApp()
activity = android.PythonActivity.setListener(app)
app.link(activity)
