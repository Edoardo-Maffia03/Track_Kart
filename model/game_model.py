from constants import (
    COLOR_PLAYER_1,
    COLOR_PLAYER_2,
    GRID_COLS,
    GRID_ROWS,
    GameState,
)
from model.car import Car
from model.circuit import Circuit, CIRCUIT_1
from model.road_tile import RoadTile
from model.grass_tile import GrassTile
from model.ice_tile import IceTile
from model.dirt_tile import DirtTile
from model.void_tile import VoidTile


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []

    def load_circuit(self) -> None:
        grid = []
        for row, line in enumerate(CIRCUIT_1):
            grid_row = []
            for col, letter in enumerate(line):
                if letter == "R":
                    grid_row.append(RoadTile(col, row))
                elif letter == "G":
                    grid_row.append(GrassTile(col, row))
                elif letter == "I":
                    grid_row.append(IceTile(col, row))
                elif letter == "D":
                    grid_row.append(DirtTile(col, row))
                elif letter == "V":
                    grid_row.append(VoidTile(col, row))
            grid.append(grid_row)
        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_cars(self) -> None:
        """Instancie les deux voitures sur leurs cases de départ."""
        self.cars = [
            Car(7, 1, player_id=1, color=COLOR_PLAYER_1),
            Car(7, 2, player_id=2, color=COLOR_PLAYER_2),
        ]

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        for car in self.cars:
            car.update_position()
