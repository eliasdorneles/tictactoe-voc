import android
from android.util import Log
from android.widget import LinearLayout
from android.widget import Button
from android.widget import TextView
from android.view import Gravity
import android.view
from tictactoe import tictactoe


class ButtonClick(implements=android.view.View[OnClickListener]):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def onClick(self, view: android.view.View) -> void:
        self.callback(*self.args, **self.kwargs)


class MyApp:
    def __init__(self):
        self._activity = android.PythonActivity.setListener(self)
        self.buttons = []
        self.top_label = None
        self.game = tictactoe.Game()
        self.message = None

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
        self.game = tictactoe.Game()
        self.message = None
        self.updateUI()

    def updateUI(self):
        if self.message:
            self.top_label.setText(self.message)
        else:
            self.top_label.setText('Player: ' + self.game.current_player)
        for i, row in enumerate(self.buttons):
            for j, button in enumerate(row):
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


def main():
    MyApp()
