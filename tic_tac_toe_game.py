from __future__ import annotations

from generic_monte_carlo import MTState, MCTS
from typing import Literal
import numpy as np

class TicTacToeState(MTState):
  def __init__(self, state):
    '''
    state should be a 3 by 3 numpy array where elements are either '1' or '-1' or 0
    '''
    self.__state = state

  def __str__(self) -> str:
    map = {1: 'o', -1: 'x', 0: '.'}
    s = ''
    for i in range(3):
      for j in range(3):
        el = self.__state[i][j]
        s += map[el] + ' '
      s += '\n'
    return s

  def game_result(self) -> Literal[1, -1, 0]:
    state = self.__state
    result = 0
    for i in range(3):
      # horizontal check
      if state[i][0] == state[i][1] \
              and state[i][1] == state[i][2]\
              and state[i][0] != 0:
        result = state[i][0]
        break
      # vertical check
      if state[0][i] == state[1][i] \
              and state[1][i] == state[2][i] \
              and state[0][i] != 0:
        result = state[0][i]
        break

    # diagonal check
    if ((state[0][0] == state[1][1] and state[1][1] == state[2][2])
            or (state[2][0] == state[1][1] and state[1][1] == state[0][2]))\
            and state[1][1] != 0:
      result = state[1][1]
    return result

  def is_terminal_state(self) -> bool:
    return self.game_result() != 0 or len(self.get_legal_actions()) == 0

  def move(self, action: list[int, int], player) -> TicTacToeState:
    new_state = self.__state.copy()
    new_state[action[0]][action[1]] = player
    return TicTacToeState(new_state)

  def get_legal_actions(self) -> list[tuple[int, int]]:
    '''
    Return a list of position that one can play
    '''
    res = []
    for i in range(3):
      for j in range(3):
        if self.__state[i][j] == 0:
          res.append((i, j))
    return res

def main():
  game_state = TicTacToeState(np.array([[1,-1,0], [0, 0, -1], [0,0,1]]))
  print("Initial")
  print(game_state)
  mcst = MCTS()
  selected_node = mcst.play(game_state)
  print("Play")
  print(selected_node.state)


if __name__ == '__main__':
  main()