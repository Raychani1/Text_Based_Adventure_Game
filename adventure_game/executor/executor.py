from io import FileIO
from typing import Any, Dict, List, Tuple, Union

from game.game import Game


class Executor:

    """Represents the Game Executor.

    Its main purpose is to set up and run the game.
    """

    def __init__(
        self,
        welcome_screen_file_path: str,
        game_data_file_path: str
    ) -> None:
        """Initializes the Executor Class.

        Args:
            welcome_screen_file_path (str): Welcome screen file path.
            game_data_file_path (str): Structured game data input file path.
        """
        # File paths
        self.__game_data_file_path: str = game_data_file_path
        self.__welcome_screen_file_path: str = welcome_screen_file_path

        # Data
        self.__data: List[
            Dict[str, Union[int, str, Dict[str, Tuple[str, int]]]]
        ] = (
            self.__process_input_data()
        )
        self.__welcome_screen_data: List[str] = self.__load_welcome_screen()

        # Game
        self.__game: Game = Game(
            game_data=self.__data,
            welcome_screen_data=self.__welcome_screen_data
        )

    def __process_input_data(self) -> List[
        Dict[str, Union[int, str, Dict[str, Tuple[str, int]]]]
    ]:
        """Processes all the data from input file.

        Returns:
            List[Dict[str, Union[int, str, Dict[str, Tuple[str, int]]]]]: 
            Processed data.
        """
        data: List[Dict[str, Union[int, str, Dict[str, Tuple[str, int]]]]] = []

        # Read data
        input_file: FileIO = open(self.__game_data_file_path, 'r')
        data_lines: List[str] = input_file.readlines()

        # Process data
        for line in data_lines:
            room_data: Dict[str, Union[int, str, List[Tuple[str, int]]]] = {}

            split_data: List[str] = line.strip().split(';')

            room_data['room_id'] = int(split_data[0])
            room_data['room_name'] = split_data[1]
            room_data['room_scenario'] = split_data[2]
            room_data['commands'] = {}

            for i in range(3, 12, 3):
                room_data['commands'][split_data[i]] = (
                    tuple([split_data[i+1], int(split_data[i+2])])
                )

            data.append(room_data)

        return data

    def __load_welcome_screen(self) -> List[str]:
        """Loads Welcome screen text.

        Returns:
            List[str]: Loaded Welcome Screen text.
        """
        # Read data
        input_file: FileIO = open(self.__welcome_screen_file_path, 'r')
        data_lines: List[str] = input_file.readlines()

        return list(map(str.strip, data_lines))

    def __call__(self, *args: Any, **kwds: Any) -> None:
        """Makes the Game Executor object callable."""
        self.__game()
