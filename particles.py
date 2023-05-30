import pygame
from support import import_folder
from random import choice


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder('./particles/magic/flame'),
            'haduken': import_folder('./particles/magic/haduken'),
            'heal': import_folder('./particles/magic/heal'),
            'shuriken': import_folder('./particles/magic/shuriken'),

            # attacks
            'claw': import_folder('./particles/monsters/monster attacks/claw'),
            'slash': import_folder('./particles/monsters/monster attacks/slash'),
            'spirit': import_folder('./particles/monsters/monster attacks/spirit'),

            # monster deaths
            'axolotl': import_folder('./particles/monsters/axolotl'),
            'octopus': import_folder('./particles/monsters/octopus'),
            'skull': import_folder('./particles/monsters/skull'),

            # flowers
            'flowers': (
                import_folder('./particles/flowers'),
                self.reflect_images(import_folder('./particles/flowers'))
            )

        }

    def reflect_images(self, frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_flower_particles(self, pos, groups):
        animation_frames = choice(self.frames['flowers'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups,)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animation()