import pygame
from constants import TILE_SIZE
#tile size is 64 which means chaque case mesure 64x64 pixels
#class RoadTile represente une seule case du circuit
class IceTile:

    def __init__(self, col: int, row: int):  #on initialise chaque case
        self.col = col
        self.row = row
        self.block = None  # bloc posé sur la case (départ, boost, ...)
        self.sprite: pygame.Surface | None = None

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:  #pour obtenir l'image de la case
        if self.sprite and self.sprite.get_width() == tile_size: #we check if it already exists and if it has the right size
            return self.sprite #if yes, we use it
        surface = pygame.Surface((tile_size, tile_size)) # creer surface graphique
        surface.fill((150, 220, 255)) 
        pygame.draw.rect(surface, (140,190,215), surface.get_rect(), 2)

        self.sprite = surface #save the image then return it
        return self.sprite