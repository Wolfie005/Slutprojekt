from random import choice
from enemy import Enemy
from magic import MagicPlayer
from particles import AnimationPlayer
from player import Player
from settings import *
from support import *
from tile import Tiles
from ui import UI
from upgrade import Upgrade
from weapon import Weapon


class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.create_map()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        self.blackjack = False

        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        """
        Creates two dictionarys one with csv files and one with tiles och setter ut tre olika delar av mappen genom
        att lägga ut tiles där csv filen säger att dem ska läggas den visar vart dem ska vara genom att använda id
        som man får av Tiled programmet. Id är platsen i deras tilesets när man importar dem in i Tiled. Sedan
        placerar jag ut playern och enemies.
         """

        layouts = {
            'border': import_csv_layout('./maps csv and png/tutorial_logic tiles.csv'),
            'flowers': import_csv_layout('./maps csv and png/tutorial_flower.csv'),
            'obstacles': import_csv_layout('./maps csv and png/tutorial_obstacle tiles.csv'),
            'entities': import_csv_layout('./maps csv and png/tutorial_entities.csv')
        }
        graphics = {
            'flowers': import_folder('./tiles/flowers'),
            'obstacles': import_folder('./tiles/obstacles')

        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col == '4':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'border':
                            Tiles((x, y), [self.obstacle_sprites], 'invisible')

                    elif col != '-1':
                        x = col_index * TILESIZE + 805
                        y = row_index * TILESIZE + 255
                        if style == 'flowers':
                            random_flower_image = choice(graphics['flowers'])
                            random_flower_image_scaled = pygame.transform.scale(random_flower_image, (32, 32))
                            Tiles((x, y),
                                  [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'flowers',
                                  random_flower_image_scaled)
                        x = col_index * TILESIZE + 90
                        y = row_index * TILESIZE + 60
                        if style == 'obstacles':
                            surf = graphics['obstacles'][int(col) - 13]
                            Tiles((x, y), [self.visible_sprites, self.obstacle_sprites], 'obstacles', surf)
                    if style == 'entities':
                        if col != '-1':
                            x = col_index * TILESIZE + 100
                            y = row_index * TILESIZE + 200
                            if col == '1':
                                self.player = Player((x, y),
                                                     [self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic)
                            else:
                                if col == '6':
                                    monster_name = 'skull'
                                elif col == '2':
                                    monster_name = 'axolotl'
                                else:
                                    monster_name = 'octopus'
                                Enemy(monster_name, (x, y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites, self.damage_player,
                                      self.trigger_death_particles,
                                      self.add_exp)

    def create_magic(self, style, strength, cost):
        """
        Creates magic sprites
        :param style:
        :param strength:
        :param cost:
        :return:
        """

        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

        if style == 'haduken':
            self.magic_player.haduken(self.player, cost, [self.visible_sprites, self.attack_sprites])

        if style == 'shuriken':
            self.magic_player.shuriken(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def create_attack(self):
        """ Creates attacks """
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        """ Destroys attacks """
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        """ Skappar logic för hur andra sprites reagerar när playern attackerar dem """
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'flowers':
                            pos = target_sprite.rect.center
                            self.animation_player.create_flower_particles(pos, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center,
                                                   [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_types):
        self.animation_player.create_particles(particle_types, pos, self.visible_sprites)

    def add_exp(self, amount):

        self.player.exp += amount

    def toggle_menu(self):

        self.game_paused = not self.game_paused

    def toggle_blackjack(self):

        self.blackjack = not self.blackjack

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 200)

        self.floor_surface = pygame.image.load('img/tutorial.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(-250, -480))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites()
                         if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
