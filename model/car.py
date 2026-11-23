import pygame
import math
from constants import (
    CAR_ACCELERATION,
    CAR_BRAKE_DECELERATION,
    CAR_HEIGHT,
    CAR_MAX_REVERSE_SPEED,
    CAR_REVERSE_ACCELERATION,
    CAR_TURN_SPEED,
    CAR_WIDTH,
    AIR_FRICTION,
    CAR_STOP_SPEED,
    DEFAULT_DRIFT_ALIGN,
    DEFAULT_DRIFT_FRICTION,
    DEFAULT_DRIFT_THRESHOLD,
    DEFAULT_GRIP_ALIGN,
    ROLLING_FRICTION,
    TILE_SIZE,
    COLOR_PLAYER_1,
)


class Car:

    def __init__(
        self,
        start_col: int,
        start_row: int,
        player_id: int = 1,
        color: tuple[int, int, int] = COLOR_PLAYER_1,
    ):
        self.player_id = player_id
        self.color = color
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.velocity_angle: float = 0.0
        self.is_drifting: bool = False
        self.current_tile = None  # case où se trouve la voiture
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        self.speed += CAR_ACCELERATION

    def update_position(self) -> None:
        # Écart angulaire ramené dans [-180°, +180°] entre orientation et vitesse
        angle_diff = (self.angle - self.velocity_angle + 180) % 360 - 180
        drift_metric = abs(angle_diff) * abs(self.speed)

        # Déclenchement et sortie automatiques du dérapage
        if abs(self.speed) < 0.5:
            self.is_drifting = False
            self.velocity_angle = self.angle
        elif not self.is_drifting:
            if drift_metric > DEFAULT_DRIFT_THRESHOLD:
                self.is_drifting = True
        else:
            if abs(angle_diff) < 5.0 and drift_metric < DEFAULT_DRIFT_THRESHOLD * 0.7:
                self.is_drifting = False

        # Réalignement progressif de la direction de vitesse vers l'orientation
        align_rate = DEFAULT_DRIFT_ALIGN if self.is_drifting else DEFAULT_GRIP_ALIGN
        self.velocity_angle = (self.velocity_angle + angle_diff * align_rate) % 360

        #Frottements de l'air: roulement ; frottements de dérapage
        if self.speed > 0.0:
            drag = AIR_FRICTION * self.speed * self.speed + ROLLING_FRICTION * self.speed
            if self.is_drifting:
                drag += DEFAULT_DRIFT_FRICTION * self.speed * (abs(angle_diff) / 45.0)
            self.speed = max(0.0, self.speed - drag)
        elif self.speed < 0.0:
            abs_speed = abs(self.speed)
            drag = AIR_FRICTION * abs_speed * abs_speed + ROLLING_FRICTION * abs_speed
            if self.is_drifting:
                drag += DEFAULT_DRIFT_FRICTION * abs_speed * (abs(angle_diff) / 45.0)
            self.speed = min(0.0, self.speed + drag)

        # Arret voiture à très faible vitesse
        if abs(self.speed) < CAR_STOP_SPEED:
            self.speed = 0.0

        # Déplacement selon la direction réelle de la vitesse (velocity_angle)
        rad = math.radians(self.velocity_angle)
        self.x += self.speed * math.cos(rad)
        self.y -= self.speed * math.sin(rad)

    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, CAR_WIDTH,
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