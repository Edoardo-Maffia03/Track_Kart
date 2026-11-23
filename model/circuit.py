from model.block import StartBlock
from model.road_tile import RoadTile
from constants import TILE_SIZE


class Circuit:

    def __init__(self,  grid: list[list[RoadTile]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def get_start_block(self, player_id: int) -> StartBlock | None:
        """Renvoie le bloc de départ du joueur, ou None s'il n'y en a pas."""
        for row in self.grid:
            for tile in row:
                if isinstance(tile.block, StartBlock) and tile.block.player_id == player_id:
                    return tile.block
        return None

    def pixel_width(self) -> int:
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        return self.rows * TILE_SIZE
