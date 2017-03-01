import android
from android.util import Log
from android.widget import LinearLayout
from android.widget import Button


class MyApp:
    def __init__(self):
        self._activity = None
        self.buttons = []

    def link(self, activity):
        self._activity = activity

    def onCreate(self):
        layout = LinearLayout(self._activity)
        layout.setOrientation(LinearLayout.VERTICAL)

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

        for row in self.buttons:
            for button in row:
                button.setText('__')
                layout.addView(button)

        self._activity.setContentView(layout)

    def onStart(self):
        print('activity onStart', self._activity)


app = MyApp()
activity = android.PythonActivity.setListener(app)
app.link(activity)
