# PlayerProjectile.py

import pygame
from Settings import *

class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface([PLAYER_PROJECTILE_WIDTH, PLAYER_PROJECTILE_HEIGHT])
        self.image.fill(PLAYER_PROJECTILE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Armazena a direção do movimento
        self.dx = dx
        self.dy = dy

    def update(self):
        """Move o projétil na direção definida e o remove se sair da tela."""
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # Remove o projétil se ele sair completamente da tela
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or \
           self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()