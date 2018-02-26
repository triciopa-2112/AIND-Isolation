"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def _game_progression(game):
    # approximate of disabled squares
    board_size = game.width * game.height
    return game.move_count / board_size


def _distance_2_center(game, move):
    x, y = move
    cx, cy = (game.width // 2, game.height // 2)

    c = math.sqrt(((x - cx) ** 2) + ((y - cy) ** 2))
    return abs(c)


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    center = _distance_2_center(game, game.get_player_location(player))
    progress = _game_progression(game)
    #print(center)
    # as the game advances, the distance to center is not as important, as there are lots of squares disabled
    if progress > .6:
        return float((own_moves - 2 * opp_moves))
    else:
        return float((own_moves - 2 * opp_moves) - center)



def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    #  aggressive always on top of opponent
    return float((own_moves - 4 * opp_moves))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # defensive move, always stay near the center
    return -1 * (_distance_2_center(game, game.get_player_location(player)))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def _min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = game.get_legal_moves()

        if (depth <= 0) or (len(moves) == 0) or (game.utility(self) != 0):
            return self.score(game, self)

        v = float("inf")

        for m in moves:
            v = min(v, self._max_value(game.forecast_move(m), depth-1))
        return v

    def _max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = game.get_legal_moves()

        if (depth <= 0) or (len(moves) == 0) or (game.utility(self) != 0):
            return self.score(game, self)

        v = float("-inf")
        for m in moves:
            v = max(v, self._min_value(game.forecast_move(m), depth-1))

        return v

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float("-inf")
        best_move = None
        try:
            for m in game.get_legal_moves():
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
                # call has been updated with a depth limit
                v = self._min_value(game.forecast_move(m), depth - 1)
                if v > best_score:
                    best_score = v
                    best_move = m
            return best_move
        except SearchTimeout:
            return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.

    """

    def _min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()

        if (depth <= 0) or (game.utility(self) != 0) or (not moves):
            return self.score(game, self)

        v = float("inf")

        for m in moves:
            v = min(v, self._max_value(game.forecast_move(m), depth-1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)

        return v

    def _max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = game.get_legal_moves()

        if (depth <= 0) or (game.utility(self) != 0) or (not moves):
            return self.score(game, self)

        v = float("-inf")
        for m in moves:
            v = max(v, self._min_value(game.forecast_move(m), depth-1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v


    def get_move(self, game, time_left):

        self.time_left = time_left
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        depth = 1
        depth_best_move = (-1, -1)
        best_move = (-1, -1)
        moves = game.get_legal_moves()

        if len(moves) > 0:
            best_move = moves[0]
        else:
            return best_move
        while True:
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.

                depth_best_move = self.alphabeta(game, depth)
                if not depth_best_move:
                    return best_move
                else:
                    best_move = depth_best_move
                depth += 1

            except SearchTimeout:
                return best_move  # Handle any actions required after timeout as needed


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = None
        moves = game.get_legal_moves()
        best_score = float("-inf")
        #if len(moves) > 0:
        #    best_move = moves[0]
        #else:
        #    return best_move

        try:

            for m in moves:
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
                v = self._min_value(game.forecast_move(m), depth - 1, alpha, beta)
                if v > best_score:
                    best_score = v
                    best_move = m
                if best_score >= beta:
                    break
                alpha = max(alpha, best_score)

            return best_move

        except SearchTimeout:
            return best_move


