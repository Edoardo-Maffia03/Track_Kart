import pygame
import math
from constants import (
    AIR_FRICTION,
    CAR_ACCELERATION,
    CAR_BRAKE_DECELERATION,
    CAR_FULL_TURN_SPEED,
    CAR_HEIGHT,
    CAR_MAX_REVERSE_SPEED,
    CAR_REVERSE_ACCELERATION,
    CAR_STOP_SPEED,
    CAR_TURN_SPEED,
    CAR_WIDTH,
    MAX_STEER_ANGLE,
    STEER_RATE,
    STEER_RETURN_RATE,
    TILE_SIZE,
)


class Car:

    def __init__(self, start_col: int, start_row: int):
        self.x: float = start_col * TILE_SIZE + TILE_SIZE / 2.0
        self.y: float = start_row * TILE_SIZE + TILE_SIZE / 2.0
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.steering_angle: float = 0.0

        # Commandes reçues sur la frame courante
        self.throttle_input: int = 0
        self.steer_input: int = 0

        self.sprite = self.build_sprite()

    def reset_inputs(self) -> None:
        """Remet à zéro les commandes avant lecture du clavier."""
        self.throttle_input = 0
        self.steer_input = 0

    def accelerate(self) -> None:
        self.throttle_input += 1

    def brake_or_reverse(self) -> None:
        """Enregistre une demande de freinage ou de marche arrière."""
        self.throttle_input -= 1

    def steer_left(self) -> None:
        """Enregistre une demande de braquage vers la gauche (sens trigonométrique)."""
        self.steer_input += 1
    def steer_right(self) -> None:
        """Enregistre une demande de braquage vers la droite."""
        self.steer_input -= 1

    def update_position(self) -> None:
        self.y += self.speed

    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect

    def brake_or_reverse(self) -> None:
        """Freine si la voiture avance, sinon marche arrière plafonnée."""
        if self.speed > 0.0:
            self.speed = max(0.0, self.speed - CAR_BRAKE_DECELERATION)
        else:
            self.speed = max(-CAR_MAX_REVERSE_SPEED, self.speed - CAR_REVERSE_ACCELERATION)
