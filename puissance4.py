from __future__ import annotations

from generic_monte_carlo import MTState, MCTS
from typing import Literal
import numpy as np

height = 6
width = 7
target = 4


class Puissance4State(MTState):
  def __init__(self, state):
    '''
    state should be a height x width numpy array where elements are either '1' or '-1' or 0
    '''
    self.__state = state

  def __str__(self) -> str:
    map = {1: 'o', -1: 'x', 0: '.'}
    s = ''
    for i in range(height):
      for j in range(width):
        el = self.__state[height - i - 1][j]
        s += map[el] + ' '
      s += '\n'
    return s

  def game_result(self) -> Literal[1, -1, 0]:
    state = self.__state
    result = 0

    # horizontal check
    for i in range(target):
      for j in range(width - target):
        unique = np.unique([state[i][j+k] for k in range(target)])
        if len(unique) == 1 and unique[0] != 0:
          return unique[0]

    # vertical check
    for j in range(width):
      for i in range(height - target):
        unique = np.unique([state[i+k][j] for k in range(4)])
        if len(unique) == 1 and unique[0] != 0:
          return unique[0]

    # first diagonal check
    for i in range(height - target):
      for j in range(width - target):
        unique = np.unique([state[i+k][j+k] for k in range(target)])
        if len(unique) == 1 and unique[0] != 0:
          return unique[0]

    # second diagonal check
    for i in range(target - 1, height):
      for j in range(target - 1, width):
        unique = np.unique([state[i-k][j-k] for k in range(target)])
        if len(unique) == 1 and unique[0] != 0:
          return unique[0]
    
    return result

  def is_terminal_state(self) -> bool:
    return self.game_result() != 0 or len(self.get_legal_actions()) == 0

  def move(self, action: list[int, int], player) -> Puissance4State:
    new_state = self.__state.copy()
    new_state[action[0]][action[1]] = player
    return Puissance4State(new_state)

  def get_legal_actions(self) -> list[tuple[int, int]]:
    '''
    Return a list of position that one can play
    '''
    res = []
    for i in range(height):
      for j in range(height):
        if self.__state[i][j] == 0 and (i == 0 or self.__state[i-1][j] != 0):
          res.append((i, j))
    return res


def main():
  game_state = Puissance4State(np.array([
    [1, -1, 1, -1,0,0,0],
    [1, -1, -1, 1,0,0,0],
    [-1, -1, 1, 1, 0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0]
  ]))
  # game_state = Puissance4State(np.array([
  #   [1, -1, 1, -1,0,0,0],
  #   [1, -1, -1, 1,0,0,0],
  #   [0, 0, 1, -1, 0,0,0],
  #   [0,0,0,0,0,0,0],
  #   [0,0,0,0,0,0,0],
  #   [0,0,0,0,0,0,0]
  # ]))
  print("Initial")
  print(game_state)
  mcst = MCTS()
  selected_node = mcst.play(game_state)
  print("Play")
  print(selected_node.state)


if __name__ == '__main__':
  main()