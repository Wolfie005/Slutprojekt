import pygame
from math import sin


class Entity(pygame.sprite.Sprite):
    """ class for Entity"""
    def __init__(self, groups):
        super().__init__(groups)

        self.frame_index = 0
        self.animation_speed = 0.15

        self.direction = pygame.math.Vector2()

    def move(self, speed):
        """
           Move the object in the specified direction with the given speed.

           Args:
               speed (float): The speed at which the object should move.

           Returns:
               None

           Raises:
               None

           Notes:
               - The object's direction must be set before calling this method.
               - The object's direction is normalized before moving.
               - The object's position is updated based on the normalized direction and speed.
               - Collision detection is performed horizontally and vertically after updating the position.
               - The object's rectangle center is updated to match the updated position.
           """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
