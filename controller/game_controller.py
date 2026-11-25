import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

            elif event.type == pygame.MOUSEBUTTONDOWN: #check if the event is a click
                print("Click detected:", event.pos)
                if self.model.state == GameState.MENU: #check if we are in the menu (not in the game for example)
                    x, y = event.pos #get the click positio,
                    cx = WINDOW_WIDTH // 2 #here we are at the center of our window
                    self.model.input = 0  # by default, no clicks



                    if 140 <= x <= 440 and 370 <= y <= 425:
                        self.model.input = 1

                    elif 584 <= x <= 884 and 370 <= y <= 425:
                        self.model.input = 2

            

    def handle_keydown(self, event) -> None:

        state = self.model.state

        if state == GameState.MENU:
            if self.model.input == 1:  # Player 1 selected
                if event.key == pygame.K_BACKSPACE:
                    self.model.player1_name = self.model.player1_name[:-1]  # Delete last letter if i press backspace
                elif event.key == pygame.K_RETURN:
                    self.model.input = 0  # Finish typing
                elif event.unicode.isprintable():
                    self.model.player1_name += event.unicode  # Add letter
            elif self.model.input == 2:  # Player 2 selected
                if event.key == pygame.K_BACKSPACE:
                    self.model.player2_name = self.model.player2_name[:-1]
                elif event.key == pygame.K_RETURN:
                    self.model.input = 0
                elif event.unicode.isprintable():
                    self.model.player2_name += event.unicode
            else:
                self.handle_menu_key(event.key)



    def handle_menu_key(self, key: int) -> None:
        if key == pygame.K_RETURN:
            self.model.load_circuit()
            self.model.state = GameState.RACING
        elif key == pygame.K_ESCAPE:
            self.quit()

    def update(self) -> None:
        if self.model.state != GameState.RACING:
            return

        for car in self.model.cars:
            player_input = self.input_handler.get_inputs(car.player_id)
            self.apply_input(car, player_input)
        self.model.update()

    def apply_input(self, car, player_input) -> None:
        if player_input["accelerate"]:
            car.accelerate()
        if player_input["brake"]:
            car.brake_or_reverse()
        if player_input["left"]:
            car.turn_left()
        if player_input["right"]:
            car.turn_right()

    def render(self) -> None:
        self.view.draw(self.model)

    def quit(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()
