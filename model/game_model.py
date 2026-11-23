from constants import (
    COLOR_PLAYER_1,
    COLOR_PLAYER_2,
    GRID_COLS,
    GRID_ROWS,
    GameState,
)
from model.block import BoostBlock, CheckpointBlock, FinishLineBlock, StartBlock
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []
        self.winner: Car | None = None

    def load_circuit(self) -> None:
        grid = [
            [RoadTile(col=col_idx, row=row_idx) for col_idx in range(GRID_COLS)]
            for row_idx in range(GRID_ROWS)
        ]
        # Circuit de test en attendant le chargement depuis un fichier
        grid[1][7].block = StartBlock(7, 1, player_id=1)
        grid[2][7].block = StartBlock(7, 2, player_id=2)
        grid[1][11].block = BoostBlock(11, 1)
        grid[2][11].block = BoostBlock(11, 2)
        grid[5][13].block = CheckpointBlock(13, 5, index=1)
        grid[5][14].block = CheckpointBlock(14, 5, index=1)
        grid[6][1].block = CheckpointBlock(1, 6, index=2)
        grid[6][2].block = CheckpointBlock(2, 6, index=2)
        grid[1][6].block = FinishLineBlock(6, 1, checkpoint_count=2)
        grid[2][6].block = FinishLineBlock(6, 2, checkpoint_count=2)

        self.circuit = Circuit(grid=grid)
        self.winner = None
        self.spawn_cars()

    def spawn_cars(self) -> None:
        """Place chaque voiture sur son bloc de départ."""
        colors = {1: COLOR_PLAYER_1, 2: COLOR_PLAYER_2}
        self.cars = []
        for player_id, color in colors.items():
            start = self.circuit.get_start_block(player_id)
            if start is None:
                continue
            self.cars.append(Car(start.col, start.row, player_id=player_id, color=color))

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        for car in self.cars:
            car.update_position()
            self.check_tile(car)
            if self.winner is None and car.laps >= self.circuit.laps_required:
                self.winner = car

    def check_tile(self, car: Car) -> None:
        """Active le bloc de la case seulement quand la voiture vient d'y entrer."""
        tile = self.circuit.get_tile_at_pixel(car.x, car.y)
        if tile is car.current_tile:
            return
        car.current_tile = tile
        if tile is not None and tile.block is not None:
            tile.block.on_car_enter(car)
