# Enemy.py

import pygame
import random
from Settings import *
from Projectile import Projectile # Importa a classe do projétil

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites_group, projectiles_group):
        super().__init__()
        # Carrega as imagens do lobo para cada direção
        self.images = {
            1: pygame.transform.scale(pygame.image.load("assets/lobodir.png").convert_alpha(), (ENEMY_WIDTH, ENEMY_HEIGHT)),
            -1: pygame.transform.scale(pygame.image.load("assets/loboesq.png").convert_alpha(), (ENEMY_WIDTH, ENEMY_HEIGHT)),
        }
        self.image = self.images[1]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Grupos de sprites para adicionar os projéteis
        self.all_sprites = all_sprites_group
        self.projectiles = projectiles_group

        # Controle de tempo para os disparos
        self.fire_rate = random.randint(ENEMY_FIRE_RATE_MIN, ENEMY_FIRE_RATE_MAX)
        self.last_shot_time = pygame.time.get_ticks() + random.randint(0, 1000) # Adiciona um atraso inicial aleatório

        # Movimento horizontal
        self.direction = random.choice([-1, 1])  # -1: esquerda, 1: direita
        self.speed = random.uniform(1.0, 2.5)

    def update(self):
        """Move o inimigo e verifica se é hora de atirar."""
        # Movimento horizontal
        self.rect.x += int(self.speed * self.direction)
        # Atualiza a imagem conforme a direção
        self.image = self.images[self.direction]
        # Inverte direção ao atingir as bordas
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = -1

        # Disparo
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