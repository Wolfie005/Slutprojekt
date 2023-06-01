import sys
import pygame
import requests
from bs4 import BeautifulSoup
from blackjack import Blackjack
from level import Level
from settings import *

html = requests.get(
    "https://weather.com/sv-SE/weather/today/l/f3b52a01b39da4a06d727feb1ee331178ebbc665753e313efa71b4c057c7b68d")
soup = BeautifulSoup(html.content, 'html.parser')
deg = soup.find("span", {"data-testid": "TemperatureValue"})

game_state = 'start'


class Game:
    """Class for Game"""
    def __init__(self):
        pygame.init()
        font = pygame.font.Font(UI_FONT, 16)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.degres = font.render(deg.text, False, 'black')
        self.degres_rect = self.degres.get_rect()
        self.degres_rect.center = (20, 100)
        pygame.display.set_caption('top-down RPG')

        self.clock = pygame.time.Clock()

        self.level = Level()

        main_sound_theme = pygame.mixer.Sound('./main_theme/13 - Mystical.ogg')
        main_sound_theme.play(loops=-1)

    def run(self):
        """
        Main game loop that handles events, updates the game state, and renders the screen.

        This function continuously runs until the game is exited. It listens for pygame events,
        such as quitting the game or key presses, and updates the game state accordingly. The
        function also updates the screen with the current game state and displays any necessary
        elements. If the game state changes to 'blackjack', it switches to the Blackjack game,
        plays a round then asks the player if it wants to play again, and then switches back to
        the main game state if the player says no.

        Args:
            self: The instance of the Game class.

        Returns:
            None
        """
        global game_state

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                    elif event.key == pygame.K_f:
                        game_state = 'blackjack'

            self.clock.tick(FPS)
            self.screen.fill('#71ddee')
            self.level.run()
            self.screen.blit(self.degres, self.degres_rect)
            if game_state == 'blackjack':
                self.screen = pygame.display.set_mode((1, 1))
                Blackjack().play()
                Blackjack().playAgain()
                self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
                game_state = 'start'
            pygame.display.update()


if game_state == 'start':
    game = Game()
    game.run()
