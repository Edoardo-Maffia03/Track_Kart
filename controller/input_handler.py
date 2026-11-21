import pygame


MAPPING = {
    pygame.K_UP: "accelerate",
    pygame.K_z: "accelerate",
    pygame.K_w: "accelerate",
    pygame.K_DOWN: "brake",
    pygame.K_s: "brake",
    pygame.K_LEFT: "left",
    pygame.K_q: "left",
    pygame.K_a: "left",
    pygame.K_RIGHT: "right",
    pygame.K_d: "right",
}


class InputHandler:

    def __init__(self):
        self.mapping = MAPPING

    def get_inputs(self) -> dict:
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
