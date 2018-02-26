"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player2 = game_agent.AlphaBetaPlayer()
        self.player1 = game_agent.MinimaxPlayer(score_fn=improved_score)
        self.game = isolation.Board(self.player1, self.player2)


    def test_play(self):
        # TODO: All methods must start with "test_"
        winner, history, outcome = self.game.play()
        print(history)
        print(winner)
        print(outcome)


if __name__ == '__main__':
    unittest.main()
