from __future__ import annotations
import numpy as np
from typing import Literal

Action = tuple[int, int]

class MTState:
  def __init__(self, game_state):
    self.game_state = game_state

  def get_legal_actions(self):
    pass

  def move(self, action) -> MTState:
    pass 

  def is_terminal_state(self) -> bool:
    pass

  def game_result() -> int:
    pass

class MonteCarloTreeSearchNode:
  def __init__(self, state: MTState, parent: MonteCarloTreeSearchNode = None, player = 1):
    self.state = state
    self.parent = parent
    self._nb_of_visits = 0
    self._results = {
      0: 0,
      1: 0,
      -1: 0
    }
    self._children = []
    self._untried_actions = self.untried_actions()
    self.player = player

  def n(self) -> int:
    '''
    returns the number that the node is visited
    '''
    return self._nb_of_visits

  def q(self) -> int:
    '''
    returns the difference between win and lose of games that go through the node
    '''
    wins = self._results[1]
    loses = self._results[-1]
    return wins - loses

  def untried_actions(self) -> list[Action]:
    '''
    compute initial untried actions, i.e. all legal action from the state
    '''
    self._untried_actions = self.state.get_legal_actions()
    return self._untried_actions

  def expand(self) -> MonteCarloTreeSearchNode:
    '''
    expand a node to a child node by using an untried action
    '''
    action = self._untried_actions.pop()
    next_state = self.state.move(action, self.player)
    next_player = -self.player
    next_node = MonteCarloTreeSearchNode(next_state, self,next_player)
    self._children.append(next_node)
    return next_node

  def best_action(self, simulation_nb) -> MonteCarloTreeSearchNode:
    for i in range(simulation_nb):
      child = self._tree_policy()
      result = child._simulate()
      child._back_propagate(result)
    return self.best_child(c_param = 0.)

  def _tree_policy(self):
    '''
    policy to choose a node to simulate a game
    try all untried action first, then choose a leaf with best rank
    '''
    current_node = self
    while not current_node._is_terminal_node():
      if len(current_node._untried_actions) > 0:
        selected_node = current_node.expand()
        return selected_node
      current_node = current_node.best_child()
    return current_node


  def _simulate(self) -> int:
    '''
    simulate a random game from this node
    '''
    state = self.state
    player = -1
    while not state.is_terminal_state():
      possible_actions = state.get_legal_actions()
      if len(possible_actions) == 0:
        return 0
      action = possible_actions[np.random.randint(len(possible_actions))]
      state = state.move(action, player)
      player = -player
    return state.game_result()

  def _is_terminal_node(self) -> bool:
    return self.state.is_terminal_state()

  def _back_propagate(self, result):
    node = self
    while node is not None:
      node._nb_of_visits +=1
      node._results[result] +=1
      node = node.parent

  def best_child(self, c_param = 1.):
    '''
    return the child with best score
    '''
    child_scores = [
        (c.q()/c.n()) + c_param * np.sqrt(np.log(self.n() / c.n()))
        for c in self._children
    ]
    return self._children[np.argmax(child_scores)]

class MCTS:
  def play(self, state: MTState):
    root = MonteCarloTreeSearchNode(state)
    selected_node = root.best_action(100)
    return selected_node

