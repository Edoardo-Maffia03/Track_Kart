import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_BRAKE_DECELERATION, 
    CAR_REVERSE_ACCELERATION, CAR_MAX_REVERSE_SPEED, CAR_TURN_SPEED, CAR_AIR_FRICTION

)


class Car:

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        self.speed += CAR_ACCELERATION

    def apply_air_friction(self) -> None:
        self.speed *= CAR_AIR_FRICTION #we multiply the speed by 0.98 to slow down the car.
        if abs(self.speed) < 0.01: 
            self.speed = 0

    def update_position(self) -> None:    # the car has un mouvement trigonometrique
        self.apply_air_friction()
        rad = math.radians(self.angle)
        self.x += self.speed * math.cos(rad) #cos is the horizontal position of the car
        self.y -= self.speed * math.sin(rad) #sin is vertically

    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, self.angle - 90) #90 parce que l'avant de la voiture est pointé vers le haut ( de base ), mtn elle a la meme direction que le mouvement
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect

    def brake_or_reverse(self) -> None:
        """Freine si la voiture avance, sinon marche arrière plafonnée."""
        if self.speed > 0.0:
            self.speed = max(0.0, self.speed - CAR_BRAKE_DECELERATION)
        else:
            self.speed = max(-CAR_MAX_REVERSE_SPEED, self.speed - CAR_REVERSE_ACCELERATION)

    def turn_left(self) -> None:   #la tourne a gauche augmente l'angle
        if self.speed > 0: 
            self.angle += CAR_TURN_SPEED
        elif self.speed < 0:
            self.angle -= CAR_TURN_SPEED

    def turn_right(self) -> None: #la tourne à droite diminue l'angle
        if self.speed > 0:
            self.angle -= CAR_TURN_SPEED
        elif self.speed < 0:
            self.angle += CAR_TURN_SPEED
