
import os
import random
import sys
from typing import Any, Dict, List, Tuple, Union

from termcolor import colored


class Game:

    """Represents the Game."""

    def __init__(
        self,
        game_data:  List[Dict[str, Union[int,
                                         str, Dict[str, Tuple[str, int]]]]],
        welcome_screen_data: List[str]
    ) -> None:
        """Initializes the Game Class.

        Args:
            game_data (List[Dict[str, Union[int, str,
            Dict[str,Tuple[str, int]]]]]): Game data.
            welcome_screen_data (List[str]): Welcome screen data.
        """
        # Data
        self.__game_data: List[
            Dict[str, Union[int, str, Dict[str, Tuple[str, int]]]]
        ] = game_data
        self.__welcome_screen_data: List[str] = welcome_screen_data

        # Room / Location
        self.__available_commands: Dict[str, Tuple[str, int]] = {}
        self.__is_previous_location_locked: bool = False

        # Player
        self.__player_name: Union[str, None] = None
        self.__player_previous_position: Union[int, None] = None
        self.__player_position: int = 0

    @staticmethod
    def __clear_terminal() -> None:
        """Clears terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def __get_player_name(self) -> None:
        """Asks for player name."""
        self.__player_name: str = input(
            colored('\nPE:ME> Do you remember your name? ', 'green')
        )
        print()

    def __move_player(self, destination: int, booby_trap_check: bool) -> None:
        """Moves player to new location.

        Args:
            destination (int): Destination room / location id.
            booby_trap_check (bool): Check for booby-traps at backwards 
            navigation.
        """
        # Check for booby-trap  trigger event
        if booby_trap_check and self.__is_previous_location_locked == False:
            booby_trap_chance: int = random.randint(0, 5)

            # Booby-trap was triggered
            if booby_trap_chance > 3:
                self.__is_previous_location_locked = True
                return

        # Move if everything is okay
        self.__player_previous_position = self.__player_position
        self.__player_position = destination

    def __welcome_screen(self) -> None:
        """Displays the welcome message."""
        self.__clear_terminal()

        for i, text in enumerate(self.__welcome_screen_data):
            if i == 0:
                print(colored(f'{text}\n', 'green'))
            else:
                print(text)
                if i == 2:
                    self.__get_player_name()

    @staticmethod
    def __get_room_id_key(
        dictionary: Dict[str, Tuple[str, int]],
        room_id: int
    ) -> str:
        """Returns dictionary key based on room id.

        Args:
            dictionary (Dict[str,Tuple[str, int]]): Dictionary containing data.
            room_id (int): Searched room id.

        Returns:
            str: Found dictionary key.
        """
        reverse_dictionary: Dict[int, str] = {}

        for key, value in dictionary.items():
            reverse_dictionary[value[1]] = key

        return reverse_dictionary[room_id]

    def __process_available_commands(self) -> None:
        """Removes command which points to the previous room.

        Returns:
            Dict[str, Tuple[str, int]]: Updated commands.
        """
        new_commands: Dict[str, Tuple[str, int]] = (
            self.__game_data[self.__player_position]['commands'].copy()
        )

        if self.__player_previous_position is not None:
            del new_commands[
                self.__get_room_id_key(
                    dictionary=new_commands,
                    room_id=self.__player_previous_position
                )
            ]

            if self.__is_previous_location_locked == True:
                self.__player_previous_position = None

        self.__available_commands = new_commands

    def __display_available_commands(self) -> None:
        """Displays available commands in current room / location."""

        spacing: str = '\t' * 4

        print(
            colored(
                f"\n{spacing}Available Commands\n{'-' * 80}\n{'Command':<21} {'Description':<40} {'Destination':<20}\n{'-' * 80}",
                'green'
            )
        )

        for key, value in self.__available_commands.items():
            command: str = key
            description: str = value[0]
            destination: str = self.__game_data[value[1]]['room_name']

            print(
                f"{colored(command, 'green'):<30} "
                f"{description:<40} {destination:<20}"
            )

        if self.__player_previous_position is not None:
            print(
                f"{colored('back', 'green'):<30} "
                f"{'Go back to the previous room':<40} "
                f"{self.__game_data[self.__player_previous_position]['room_name']:<20}"
            )

    def __get_command(self) -> None:
        """Reads command from player.

        Args:
            commands (Dict[str, Tuple[str, int]]): Available commands.
        """
        command: str = ""
        destination: int = -1

        # Wait for valid command
        while (command not in self.__available_commands.keys()):
            command: str = input(
                colored(
                    f'\nPE:ME> What should we do now {self.__player_name}? ',
                    'green'
                )
            ).lower()

            if self.__player_previous_position is not None and command == 'back':
                destination = self.__player_previous_position
                break

            if command == 'exit':
                sys.exit()

        # Valid command
        if destination == -1:
            destination = self.__available_commands[command][1]

        self.__move_player(
            destination=destination,
            booby_trap_check=(destination == self.__player_previous_position)
        )

        # Clear terminal
        self.__clear_terminal()

    def __display_room(self) -> None:
        """Displays current room / location."""
        if self.__is_previous_location_locked:
            print(
                colored(
                    "It looks like you've triggered a booby-trap. "
                    "You can't go that way this turn.\n",
                    'red'
                )
            )

        self.__process_available_commands()

        self.__is_previous_location_locked = False

        print(
            f"\n{colored('Location:', 'green')} "
            f"{self.__game_data[self.__player_position]['room_name']}"
        )
        print(
            f"\n{colored('Scenario:', 'green')} "
            f"\n{self.__game_data[self.__player_position]['room_scenario']}"
        )
        self.__display_available_commands()
        self.__get_command()

    def __call__(self, *args: Any, **kwds: Any) -> None:
        """Makes the Game object callable."""
        self.__welcome_screen()

        # While the player is in the dungeon
        while self.__player_position != 7:
            self.__display_room()

        # On successful escape
        print(
            colored(
                f"Congratulations {self.__player_name}! You've made it out "
                f'alive from the dungeon. Be careful next time. Cheers!',
                'green'
            )
        )
