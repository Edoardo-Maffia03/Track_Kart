import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel


class GameView:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, model: GameModel) -> None:
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        pygame.display.flip()

    def _draw_menu(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2
        pygame.draw.rect(self.screen, (180, 55, 75),
                 (0, 0, WINDOW_WIDTH // 2, WINDOW_HEIGHT))
        pygame.draw.rect(self.screen, (45, 95, 175),
                 (WINDOW_WIDTH // 2, 0, WINDOW_WIDTH // 2, WINDOW_HEIGHT)) 
        pygame.draw.rect(self.screen, (45, 95, 175), #player 1 
                 (100, 260, 380, 280), border_radius=15)
        
        pygame.draw.rect(self.screen, (180, 55, 75), #player 2
                 (544, 260, 380, 280), border_radius=15)

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [
            ("PLAYER 1 : " + model.player1_name, None),
            ("PLAYER 2 : " + model.player2_name, None),
            ("CIRCUIT : 1", None),
            ("START RACE (Enter)", GameState.RACING),
            ("QUIT", None)
]
        
        for i, (label, _) in enumerate(options):
            if i == 0:  # Player 1
                rect = pygame.Rect(140, 370, 300, 55)

            elif i == 1:  # Player 2
                rect = pygame.Rect(584, 370, 300, 55)

            elif i == 2:  # Circuit
                rect = pygame.Rect(cx - 150, 200, 300, 50)

            elif i == 3:  # Start Race
                rect = pygame.Rect(cx - 150, 590, 300, 60)

            else:  # Quit
                rect = pygame.Rect(cx - 100, 680, 200, 50)
            # Draw button
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)

            # Yellow border for selected player
            if model.input == i + 1 and i < 2:
                pygame.draw.rect(self.screen, COLOR_ACCENT, rect, 3)

            # Display text
            text = self.font.render(label, True, COLOR_TEXT)
            self.screen.blit(text, text.get_rect(center=rect.center))

    def _draw_racing(self, model: GameModel) -> None:
        if model.circuit is None:
            return

        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                x, y = col_idx * TILE_SIZE, row_idx * TILE_SIZE
                self.screen.blit(tile.get_sprite(TILE_SIZE), (x, y))
                if tile.block is not None:
                    self._draw_block(tile.block, x, y)

        for car in model.cars:
            surf, rect = car.get_rotated_sprite()
            self.screen.blit(surf, rect)

    def _draw_block(self, block, x: int, y: int) -> None:
        """Dessine un bloc : un carré de couleur avec sa lettre."""
        rect = pygame.Rect(x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8)
        pygame.draw.rect(self.screen, block.color, rect, border_radius=6)
        text = self.font.render(block.label, True, COLOR_TEXT)
        self.screen.blit(text, text.get_rect(center=rect.center))
            
        
