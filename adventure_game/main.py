import os
import sys

from executor.executor import Executor


def run_game(
    welcome_screen_file_path: str = os.path.join(
        os.getcwd(), 'adventure_game', 'data', 'welcome_screen.txt'
    ),
    game_data_file_path: str = os.path.join(
        os.getcwd(), 'adventure_game', 'data', 'adventure_game.csv'
    ),
) -> None:
    """Executes game based on files sent through arguments.

    Args:
        welcome_screen_file_path (str, optional): Welcome Screen Text. Defaults
        to f'{os.getcwd()}/adventure_game/data/welcome_screen.txt'.
        game_data_file_path (str, optional): Game Configuration File. Defaults 
        to f'{os.getcwd()}/adventure_game/data/adventure_game.csv'.
    """
    game_executor: Executor = Executor(
        welcome_screen_file_path=welcome_screen_file_path,
        game_data_file_path=game_data_file_path,
    )

    game_executor()


if __name__ == '__main__':
    run_game() if len(sys.argv) != 3 else run_game(sys.argv[1], sys.argv[2])
