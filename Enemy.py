# Enemy.py

import pygame
import random
from Settings import *
from Projectile import Projectile # Importa a classe do projétil

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites_group, projectiles_group):
        super().__init__()
        self.image = pygame.Surface([ENEMY_WIDTH, ENEMY_HEIGHT])
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Grupos de sprites para adicionar os projéteis
        self.all_sprites = all_sprites_group
        self.projectiles = projectiles_group

        # Controle de tempo para os disparos
        self.fire_rate = random.randint(ENEMY_FIRE_RATE_MIN, ENEMY_FIRE_RATE_MAX)
        self.last_shot_time = pygame.time.get_ticks() + random.randint(0, 1000) # Adiciona um atraso inicial aleatório

    def update(self):
        """Verifica se é hora de atirar."""
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.fire_rate:
            self.shoot()
            self.last_shot_time = now

    def shoot(self):
        """Cria um novo projétil."""
        # O projétil sai da base do inimigo
        projectile = Projectile(self.rect.centerx, self.rect.bottom)
        self.all_sprites.add(projectile)
        self.projectiles.add(projectile)