import tkinter as tk
from tkinter import font
from itertools import cycle
import numpy as np

from typing import NamedTuple

from puissance4 import Puissance4State
from generic_monte_carlo import MCTS


class Player(NamedTuple):
  label: str
  color: str
  value: int
  name: str
  type: str


class Move(NamedTuple):
  row: int
  col: int
  label: str = ""


DEFAULT_PLAYERS = (
    Player(label="O", color="red", value=-1, name="You", type='human'),
    Player(label="O", color="blue", value=1, name="AI", type='AI'),
)


class Puissance4Game:
  def __init__(self, players=DEFAULT_PLAYERS):
    self._players = cycle(players)
    self.current_player = next(self._players)
    self.winner_combo = []
    self._current_moves = []
    self._has_winner = False
    self._winning_combos = []
    self.state = Puissance4State(np.zeros((6, 7)))
    # self._setup_board()

  def is_valid_move(self, move) -> bool:
    """Return True if move is valid, and False otherwise."""
    action = [move.row, move.col]
    return not self.state.is_terminal_state() and self.state.is_legal_action(action)

  def process_move(self, move):
    action = [move.row, move.col]
    self.state = self.state.move(action, self.current_player.value)

  def has_winner(self) -> bool:
    state = self.state
    return state.is_terminal_state() and state.game_result() != 0

  def is_tied(self) -> bool:
    state = self.state
    return state.is_terminal_state() and state.game_result() == 0

  def toggle_player(self):
    """Return a toggled player."""
    self.current_player = next(self._players)


class Puissance4Board(tk.Tk):
  def __init__(self, game: Puissance4Game):
    super().__init__()
    self.title("Puissance 4")
    self._cells = {}
    self._buttons = [[0] * 7 for i in range(6)]
    self._create_board_display()
    self._create_board_grid()
    self._game = game

  def _create_board_display(self):
    display_frame = tk.Frame(master=self)
    display_frame.pack()

    self.display = tk.Label(
        master=display_frame,
        text="Ready?",
        font=font.Font(size=28, weight="bold"),
    )

    self.display.pack()

  def _create_board_grid(self):
    grid_frame = tk.Frame(master=self)
    grid_frame.pack(pady=30)
    for row in range(6):
      self.rowconfigure(row, weight=1, minsize=20)
      self.columnconfigure(row, weight=1, minsize=20)
      for col in range(7):
          button = tk.Button(
              master=grid_frame,
              text="",
              font=font.Font(size=18, weight="bold"),
              fg="black",
              width=3,
              height=2,
              highlightbackground="lightblue",
          )
          self._buttons[row][col] = button
          self._cells[button] = (row, col)
          button.bind("<ButtonPress-1>", self.play)

          button.grid(
              row=row,
              column=col,
              padx=5,
              pady=5,
              sticky="nsew"
          )

  def play(self, event):
    """Handle a player's move."""
    if self._game.current_player.type == 'human':
      clicked_btn = event.widget
      row, col = self._cells[clicked_btn]
      move = Move(row, col, self._game.current_player.label)
      self._move_and_update(move, clicked_btn=clicked_btn)

    # AI plays
    if self._game.current_player.type == 'AI' and not self._game.state.is_terminal_state():
      mcts = MCTS()
      selected_node = mcts.play(self._game.state, simulation_nb=500)
      state = self._game.state
      new_state = selected_node.state
      action = None
      for i in range(6):
        for j in range(7):
          if new_state.state[i][j] != state.state[i][j]:
            action = [i, j]
            break
      move = Move(action[0], action[1], self._game.current_player.label)
      self._move_and_update(move, self._buttons[action[0]][action[1]])

  def _move_and_update(self, move: Move, clicked_btn=None):
    if self._game.is_valid_move(move):
      self._update_button(clicked_btn)
      self._game.process_move(move)
      if self._game.is_tied():
        self._update_display(msg="Tied game!", color="red")
      elif self._game.has_winner():
        self._highlight_cells()
        msg = f'Player "{self._game.current_player.color}" won!'
        color = self._game.current_player.color
        self._update_display(msg, color)
      else:
        self._game.toggle_player()
        msg = f"{self._game.current_player.color}'s turn"
        self._update_display(msg)
      self.update()

  def _update_button(self, clicked_btn):
    clicked_btn.config(fg=self._game.current_player.color)
    clicked_btn.config(text=self._game.current_player.label)

  def _update_display(self, msg, color="black"):
    self.display["text"] = msg
    self.display["fg"] = color

  def _highlight_cells(self):
    for button, coordinates in self._cells.items():
        if coordinates in self._game.winner_combo:
            button.config(highlightbackground="red")


def main():
    """Create the game's board and run its main loop."""
    game = Puissance4Game()
    board = Puissance4Board(game)
    board.geometry('800x700+50+50')
    board.mainloop()


if __name__ == "__main__":
    main()
