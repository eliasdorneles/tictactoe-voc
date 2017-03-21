from tictactoe import tictactoe
import unittest
# XXX: tests are currently broken, because of importing

class GameTest(unittest.TestCase):
    def setUp(self):
        # called before every test
        self.game = tictactoe.Game()
    def test_create_game(self):
        self.assertIsNotNone(self.game)
    def test_play(self):
        self.game.play(0,0)
        # self.assertEquals(self.game.board[0][0], 'O')
        self.game.play(1,0)
        self.game.play(1,1)
        self.game.play(2,0)
        with self.assertRaisesRegexp(ValueError, "winner"):
            self.game.play(2,2)
    def test_play_twice(self):
        self.game.play(0,0)
        with self.assertRaisesRegexp(ValueError, "invalid"):
            self.game.play(0,0)
    def test_full_board(self):
        self.game.play(0,0)
        self.game.play(1,0)
        self.game.play(2,0)
        self.game.play(1,1)
        self.game.play(0,1)
        self.game.play(0,2)
        self.game.play(2,1)
        self.game.play(2,2)
        with self.assertRaisesRegexp(ValueError, "loosers"):
            self.game.play(1,2)

