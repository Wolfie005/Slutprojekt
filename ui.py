import pygame
from settings import *


class UI:
    """ class for UI"""
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        """
        Draws a bar on the display surface representing the current progress or amount.

        Args:
            self (object): The current instance of the class.
            current (int): The current progress or amount.
            max_amount (int): The maximum progress or amount.
            bg_rect (pygame.Rect): The background rectangle where the bar will be drawn.
            color (tuple or pygame.Color): The color of the bar.

        Returns:
            None

        Example:
            show_bar(self, 75, 100, pygame.Rect(10, 10, 200, 20), (255, 0, 0))
        """

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        """
            Displays the given experience points (exp) on the display surface.

            Args:
                exp (int): The experience points to be displayed.

            Returns:
                None
            """
        text_surf = self.font.render(str(int(exp)), False, EXP_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(15, 5))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(15, 5), 3)

    def selection_box(self, left, top, has_switched):
        """
           Draws a selection box on the display surface at the specified position with the given switch status.

           Args:
               self: The instance of the class calling the function.
               left (int): The x-coordinate of the top-left corner of the selection box.
               top (int): The y-coordinate of the top-left corner of the selection box.
               has_switched (bool): A flag indicating whether the selection box has switched.

           Returns:
               pygame.Rect: The rectangle object representing the background of the selection box.

           Note:
               - The function assumes the existence of a Pygame display surface.
               - ITEM_BOX_SIZE, UI_BG_COLOR, UI_BORDER_COLOR, and UI_BORDER_COLOR_ACTIVE are assumed to be predefined.

           """

        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        """
          Overlay a weapon graphic on the display surface.

          Args:
              weapon_index (int): The index of the weapon graphic in the list of weapon graphics.
              has_switched (bool): A flag indicating whether the weapon has been switched or not.

          Returns:
              None

          """
        bg_rect = self.selection_box(10, 630, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        """
           Overlay a magic graphic onto the display surface.

           Args:
               magic_index (int): The index of the magic graphic in the self.magic_graphics list.
               has_switched (bool): A flag indicating whether the selection box has switched.

           Returns:
               None

           Raises:
               None

           This function overlays a magic graphic onto the display surface at the center of the selection box.
           It takes the magic_index to determine the graphic from the self.magic_graphics list and the has_switched flag
           to determine the position of the selection box. The selection box is created using the self.selection_box method.
           The magic graphic is then blitted onto the display surface using the blit method.

           """
        bg_rect = self.selection_box(70, 640, has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        """
            Display the player's health and energy bars, experience points, weapon overlay, and magic overlay on the screen.

            Parameters:
                player (Player): The player object containing information about the player's status and progress.

            Returns:
                None

            Side Effects:
                - Renders the player's health and energy bars on the screen.
                - Renders the player's experience points on the screen.
                - Renders the weapon overlay on the screen based on the player's current weapon index and switch availability.
                - Renders the magic overlay on the screen based on the player's current magic index and switch availability.
            """
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
