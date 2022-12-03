from puissance4 import Puissance4State
import numpy as np


class TestPuissance4:
  def test_non_terminal_state(self):
    game_state = Puissance4State(np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, -1, 1, -1, 0, 0, 0],
        [1, -1, -1, 1, 0, 0, 0],
        [-1, -1, 1, 1, 0, 0, 0]
    ]))

    assert game_state.is_terminal_state() == False

  def test_terminal_state_win_row(self):
    game_state = Puissance4State(np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, -1, -1, -1]
    ]))

    assert game_state.is_terminal_state() == True
    assert game_state.game_result() == 1

  def test_terminal_state_win_diagonal_nw_se(self):
    game_state = Puissance4State(np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 1, -1, -1, 0, 0, 0],
        [1, -1, 1, -1, 0, 0, 0],
        [-1, -1, 1, 1, 0, 0, 0]
    ]))

    assert game_state.is_terminal_state() == True
    assert game_state.game_result() == 1

  def test_terminal_state_win_diagonal_nw_se_right(self):
    game_state = Puissance4State(np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, -1, -1],
        [0, 0, 0, 1, -1, 1, -1],
        [0, 0, 0, -1, -1, 1, 1]
    ]))

    assert game_state.is_terminal_state() == True
    assert game_state.game_result() == 1

  def test_terminal_state_win_diagonal_sw_ne(self):
    game_state = Puissance4State(np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, -1, 0, 0, 0],
        [1, 1, -1, -1, 0, 0, 0],
        [1, -1, -1, 1, 0, 0, 0],
        [-1, -1, 1, 1, 0, 0, 0]
    ]))

    assert game_state.is_terminal_state() == True
    assert game_state.game_result() == -1

  def test_terminal_state_win_diagonal_sw_ne_right(self):
    game_state = Puissance4State(np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, -1],
        [0, 0, 0, 1, 1, -1, -1],
        [0, 0, 0, 1, -1, -1, 1],
        [0, 0, 0, -1, -1, 1, 1]
    ]))

    assert game_state.is_terminal_state() == True
    assert game_state.game_result() == -1
