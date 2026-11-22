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

    def get_forward_vector(self) -> tuple[float, float]:
        """Retourne le vecteur unitaire orienté vers l'avant de la voiture."""
        rad = math.radians(self.angle)
        return math.cos(rad), -math.sin(rad)
    def update_position(self, dt: float) -> None:
        """Met à jour le braquage, l'orientation, la vitesse et la position."""
        fx, fy = self.get_forward_vector()
        v_forward = self.vx * fx + self.vy * fy
        current_speed = math.hypot(self.vx, self.vy)
        # 1. Mise à jour de l'angle de braquage des roues
        if self.steer_input != 0:
            self.steering_angle += self.steer_input * STEER_RATE * dt
            if self.steering_angle > MAX_STEER_ANGLE:
                self.steering_angle = MAX_STEER_ANGLE
            elif self.steering_angle < -MAX_STEER_ANGLE:
                self.steering_angle = -MAX_STEER_ANGLE
        else:
            # Retour progressif des roues vers l'axe central
            if abs(self.steering_angle) <= STEER_RETURN_RATE * dt:
                self.steering_angle = 0.0
            elif self.steering_angle > 0.0:
                self.steering_angle -= STEER_RETURN_RATE * dt
            else:
                self.steering_angle += STEER_RETURN_RATE * dt
        # 2. Rotation du châssis (inversée en marche arrière)
        if current_speed > 2.0:
            turn_factor = min(1.0, current_speed / CAR_FULL_TURN_SPEED)
            dir_sign = 1.0 if v_forward >= -1.0 else -1.0
            omega_deg = (
                (self.steering_angle / MAX_STEER_ANGLE)
                * CAR_TURN_SPEED
                * turn_factor
                * dir_sign
            )
            self.angle = (self.angle + omega_deg * dt) % 360.0
        # Recalcul du vecteur avant après la rotation
        fx, fy = self.get_forward_vector()
        # 3. Accélération longitudinale, freinage ou marche arrière
        longitudinal_accel = 0.0
        if self.throttle_input > 0:
            longitudinal_accel = CAR_ACCELERATION
        elif self.throttle_input < 0:
            if v_forward > 12.0:
                longitudinal_accel = -CAR_BRAKE_DECELERATION
            elif v_forward > -CAR_MAX_REVERSE_SPEED:
                longitudinal_accel = -CAR_REVERSE_ACCELERATION
        v_forward += longitudinal_accel * dt
        if self.throttle_input < 0 and v_forward < -CAR_MAX_REVERSE_SPEED:
            v_forward = -CAR_MAX_REVERSE_SPEED
        # 4. Reconstruction du vecteur vitesse et frottements de l'air
        self.vx = v_forward * fx
        self.vy = v_forward * fy
        speed = math.hypot(self.vx, self.vy)
        if speed > 0.0:
            air_drag = AIR_FRICTION * speed * speed
            new_speed = max(0.0, speed - air_drag * dt)
            if new_speed < CAR_STOP_SPEED and self.throttle_input == 0:
                new_speed = 0.0
            scale = new_speed / speed
            self.vx *= scale
            self.vy *= scale
            self.speed = new_speed
        else:
            self.speed = 0.0
        # 5. Mise à jour de la position
        self.x += self.vx * dt
        self.y += self.vy * dt
    def build_sprite(self) -> pygame.Surface:
        """Construit le sprite horizontal de la voiture (avant orienté à droite)."""
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (235, 60, 60), (0, 0, CAR_WIDTH, CAR_HEIGHT), border_radius=4)
        # Phares à l'avant pour distinguer immédiatement l'orientation
        pygame.draw.circle(surf, (255, 250, 170), (CAR_WIDTH - 3, 4), 2)
        pygame.draw.circle(surf, (255, 250, 170), (CAR_WIDTH - 3, CAR_HEIGHT - 4), 2)
        return surf
    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Retourne le sprite pivoté selon l'angle trigonométrique courant."""
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
