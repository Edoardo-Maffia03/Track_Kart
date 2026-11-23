from constants import (
    COLOR_PLAYER_1,
    COLOR_PLAYER_2,
    GRID_COLS,
    GRID_ROWS,
    GameState,
)
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []

    def load_circuit(self) -> None:
        grid = [
            [RoadTile(col=col_idx, row=row_idx) for col_idx in range(GRID_COLS)]
            for row_idx in range(GRID_ROWS)
        ]
        self.circuit = Circuit(grid=grid)
        self.spawn_cars()

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
