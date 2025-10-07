import pygame
from Settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("assets/sopro.png").convert_alpha()
        self.image = pygame.transform.scale(img, (PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        """Move o projétil para baixo e o remove se sair da tela."""
        self.rect.y += PROJECTILE_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() # Remove o sprite se ele sair da tela