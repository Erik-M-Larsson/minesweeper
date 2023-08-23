import numpy as np

from game import Game


class Agent_AI:
    def __init__(self, game: Game) -> None:
        self.game = game

    def play(self) -> None:
        """Chose one cell and which mouse button to click.
        For now the choice is random"""

        # TODO reinforcement learning algorithm

        # Input

        n_cells = self.game.rows * self.game.columns
        symbols = [
            "unknown",
            "empty",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "flag",
            ["mine", "red_mine"],
            "x_mine",
        ]
        input_shape = (n_cells * len(symbols)) + 2  # +2 for time and mines counter
        self._matrix = np.random.rand(n_cells * 2, input_shape) * 2 - 1

        input = np.zeros(input_shape, np.int16)

        board_status = np.array(self.game.get_board_status())

        for index, symbol in enumerate(symbols):
            if isinstance(symbol, list):
                is_symbol = np.logical_or(
                    board_status == symbol[0], board_status == symbol[1]
                )
            else:
                is_symbol = board_status == symbol

            input[index * n_cells : (index + 1) * n_cells] = is_symbol

        if input.sum() != n_cells:
            raise Exception(
                f"Catastrophe total! Number of cells on board, {n_cells}, not equal to to total number of symbols, {input.sum()}."
            )

        input[-2] = self.game.get_mines_count()
        input[-1] = self.game.get_time_count()

        # Deep thought
        output = self._matrix @ input

        # Convert output to row, col and mouse_button
        best_choice = output.argmax()
        cell = best_choice % n_cells
        row, col = cell // self.game.columns, cell % self.game.columns
        mouse_button = "left" if best_choice // n_cells == 0 else "right"

        print(row, col, mouse_button)
        self.game.play(row, col, mouse_button)
