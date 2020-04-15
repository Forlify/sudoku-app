from src.state import State
import src.utils.utils as utils


# TODO: improve import (file format + better window + change font color)

def main():
    initial_sudoku_numbers = [[None, 8, None, None, 1, 3, 4, None, None],
                              [4, 2, 3, 6, 8, None, None, None, None],
                              [None, 7, 1, None, 5, 4, None, 8, 3],
                              [1, 9, None, None, None, 8, 7, None, None],
                              [None, 4, 7, None, None, 2, 5, None, 8],
                              [None, 5, None, None, None, 9, None, 3, None],
                              [2, None, 9, 3, None, 5, None, 7, None],
                              [5, None, None, 7, 2, None, None, None, 9],
                              [7, 3, None, None, None, None, 2, None, 6]]
    state = State(initial_sudoku_numbers)

    while True:
        state.app.update()

        if utils.window_width != state.app.winfo_width() or utils.window_height != utils.window_height:
            if state.app.winfo_width() * 2 / 3 > state.app.winfo_height():
                utils.window_width = int(state.app.winfo_height() * 3 / 2)
                utils.window_height = state.app.winfo_height()
            else:
                utils.window_width = state.app.winfo_width()
                utils.window_height = int(state.app.winfo_width() * 2 / 3)

            state.app.geometry(str(utils.window_width) + "x" + str(utils.window_height))
            state.actualize_font()
            state.place()


if __name__ == "__main__":
    main()
