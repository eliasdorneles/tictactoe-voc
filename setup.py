from setuptools import setup


setup(
    name='tictactoe',
    version='0.0.1',
    packages=['tictactoe'],
    options={
        'app': {
            'formal_name': 'TicTacToe',
            'bundle': 'org.pybee.demo',
        }
    }
)
