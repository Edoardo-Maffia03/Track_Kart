from constants import (
    COLOR_PLAYER_1,
    COLOR_PLAYER_2,
    GRID_COLS,
    GRID_ROWS,
    GameState,
)
from model.block import BoostBlock, CheckpointBlock, FinishLineBlock, StartBlock
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
        self.winner: Car | None = None

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
        # Blocs placés à la main sur CIRCUIT_1 (en attendant une grille de blocs)
        grid[1][4].block = StartBlock(4, 1, player_id=1)
        grid[2][4].block = StartBlock(4, 2, player_id=2)
        grid[1][3].block = FinishLineBlock(3, 1, checkpoint_count=3)
        grid[2][3].block = FinishLineBlock(3, 2, checkpoint_count=3)
        grid[1][9].block = BoostBlock(9, 1)
        grid[2][9].block = BoostBlock(9, 2)
        grid[3][13].block = CheckpointBlock(13, 3, index=1)
        grid[3][14].block = CheckpointBlock(14, 3, index=1)
        grid[7][8].block = CheckpointBlock(8, 7, index=2)
        grid[7][9].block = CheckpointBlock(9, 7, index=2)
        grid[6][1].block = CheckpointBlock(1, 6, index=3)
        grid[6][2].block = CheckpointBlock(2, 6, index=3)

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
