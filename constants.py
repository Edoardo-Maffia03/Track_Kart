WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 0.05
CAR_WIDTH = 30
CAR_HEIGHT = 50

CAR_BRAKE_DECELERATION = 0.12
CAR_REVERSE_ACCELERATION = 0.04
CAR_MAX_REVERSE_SPEED = 2.5
CAR_TURN_SPEED = 3.0 

# Frottements de l'air et paramètres de dérapage (route)
AIR_FRICTION = 0.0018
ROLLING_FRICTION = 0.004
CAR_STOP_SPEED = 0.02
DEFAULT_DRIFT_THRESHOLD = 32.0  # seuil de dérapage
DEFAULT_GRIP_ALIGN = 0.25       # réalignement rapide hors dérapage
DEFAULT_DRIFT_ALIGN = 0.06      # réalignement lent en dérapage (glisse visible)
DEFAULT_DRIFT_FRICTION = 0.025  # frottement supplémentaire en dérapage

# Blocs
BOOST_SPEED = 3.0  # vitesse ajoutée par un boost


class GameState:
    MENU = "menu"
    RACING = "racing"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
COLOR_PLAYER_1 = (235, 65, 65)
COLOR_PLAYER_2 = (65, 145, 245)
COLOR_BLOCK_START = (110, 110, 120)
COLOR_BLOCK_BOOST = (240, 160, 40)
