# Player.py

import pygame
import math
from Settings import *
from PlayerProjectile import PlayerProjectile

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Imagem original para rotação sem perda de qualidade
        self.original_image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT], pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, GREEN, [(PLAYER_WIDTH / 2, 0), (0, PLAYER_HEIGHT), (PLAYER_WIDTH, PLAYER_HEIGHT)])
        
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        self.dx = 0
        self.dy = 0
        self.angle = 0
        self.lives = PLAYER_MAX_LIVES

        # Gerenciamento de Munição
        self.ammo = {1: 0, 2: 0, 3: 0}
        self.selected_slot = 1
        
        self.reset_stats()

    def reset_ammo(self):
        """Reseta a munição para o início de uma fase."""
        self.ammo[1] = PLAYER_STARTING_AMMO
        self.ammo[2] = 0
        self.ammo[3] = 0
        self.selected_slot = 1

    def select_slot(self, slot_num):
        """Muda o slot de projétil selecionado."""
        if slot_num in self.ammo:
            self.selected_slot = slot_num

    def shoot(self, all_sprites_group, player_projectiles_group):
        """Dispara um projétil na direção em que o jogador está olhando."""
        if self.ammo[self.selected_slot] > 0:
            self.ammo[self.selected_slot] -= 1
            
            # Ajusta o ângulo do jogador para o sistema trigonométrico padrão (0 graus = direita)
            angle_rad = math.radians(self.angle + 90)
            
            # Calcula o vetor de movimento do projétil
            proj_dx = math.cos(angle_rad) * PLAYER_PROJECTILE_SPEED
            proj_dy = -math.sin(angle_rad) * PLAYER_PROJECTILE_SPEED # Y é negativo para mover para cima

            # Calcula a posição exata da "ponta" do jogador para o projétil surgir
            tip_offset_x = math.sin(math.radians(self.angle)) * (PLAYER_HEIGHT / 2)
            tip_offset_y = -math.cos(math.radians(self.angle)) * (PLAYER_HEIGHT / 2)
            spawn_x = self.rect.centerx + tip_offset_x
            spawn_y = self.rect.centery + tip_offset_y
            
            projectile = PlayerProjectile(spawn_x, spawn_y, proj_dx, proj_dy)
            all_sprites_group.add(projectile)
            player_projectiles_group.add(projectile)

    def reset_stats(self):
        """Reseta todas as estatísticas para um novo jogo."""
        self.lives = PLAYER_MAX_LIVES
        self.reset_ammo()
        self.reset_position()

    def lose_life(self):
        """Reduz uma vida e reposiciona o jogador."""
        if self.lives > 0:
            self.lives -= 1
        self.reset_position()

    def reset_position(self):
        """Retorna o jogador à posição inicial."""
        self.rect.centerx = PLAYER_START_X + PLAYER_WIDTH / 2
        self.rect.bottom = PLAYER_START_Y + PLAYER_HEIGHT
        self.angle = 0
        self.dx = 0
        self.dy = 0

    def set_speed(self, dx, dy):
        """Define a velocidade de movimento do jogador."""
        self.dx = dx
        self.dy = dy

    def update(self):
        """Atualiza a posição e a rotação do jogador."""
        # Atualiza o ângulo apenas se houver movimento
        if self.dx != 0 or self.dy != 0:
            self.angle = math.degrees(math.atan2(-self.dy, self.dx)) - 90
        
        # Rotaciona a imagem original para evitar distorção
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)

        # Move o jogador
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # Mantém o jogador dentro da tela
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT