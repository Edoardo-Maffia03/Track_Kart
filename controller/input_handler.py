import pygame


MAPPING_P1 = {
    pygame.K_z: "accelerate",
    pygame.K_w: "accelerate",
    pygame.K_s: "brake",
    pygame.K_q: "left",
    pygame.K_a: "left",
    pygame.K_d: "right",
}

MAPPING_P2 = {
    pygame.K_UP: "accelerate",
    pygame.K_DOWN: "brake",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
}


class InputHandler:

    def __init__(self):
        self.mappings = {1: MAPPING_P1, 2: MAPPING_P2}

    def get_inputs(self, player_id: int = 1) -> dict[str, bool]:
        keys = pygame.key.get_pressed()
        mapping = self.mappings.get(player_id, MAPPING_P1)
        p = {action: False for action in mapping.values()}

        for key, action in mapping.items():
            if keys[key]:
                p[action] = True

        return p
