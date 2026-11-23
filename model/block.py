from abc import ABC, abstractmethod

from constants import BOOST_SPEED, COLOR_BLOCK_BOOST, COLOR_BLOCK_START


class Block(ABC):
    """Bloc posé sur une case du circuit (départ, boost, ...)."""

    color = (255, 255, 255)
    label = ""

    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row

    @abstractmethod
    def on_car_enter(self, car) -> None:
        """Effet du bloc quand une voiture arrive sur sa case."""


class StartBlock(Block):
    """Position de départ d'un joueur."""

    color = COLOR_BLOCK_START

    def __init__(self, col: int, row: int, player_id: int):
        super().__init__(col, row)
        self.player_id = player_id
        self.label = str(player_id)

    def on_car_enter(self, car) -> None:
        pass  # pas d'effet pendant la course


class BoostBlock(Block):
    """Donne un coup d'accélération à la voiture."""

    color = COLOR_BLOCK_BOOST
    label = "B"

    def on_car_enter(self, car) -> None:
        car.speed += BOOST_SPEED
