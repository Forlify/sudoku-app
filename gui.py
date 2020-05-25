from src.state import State
import src.utils.utils as utils


def main():
    # Start with empty sudoku:
    initial_sudoku_numbers = [[None] * 9] * 9
    state = State(initial_sudoku_numbers)

    # App responsiveness:
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
