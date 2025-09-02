# main.py

import pygame
import sys
import random
from Settings import *
from Player import Player
from Car import Car
from Button import Button
from Enemy import Enemy
from Projectile import Projectile
from PlayerProjectile import PlayerProjectile

# --- Estados do Jogo ---
GAME_STATE_PLAYING = 0
GAME_STATE_GAME_OVER = 1
GAME_STATE_ALL_CLEARED = 2

# --- Inicialização ---
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Frogger Aprimorado")
clock = pygame.time.Clock()

# --- Variáveis e Grupos ---
life_lost_feedback_time = 0
all_sprites = pygame.sprite.Group()
cars_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
enemy_projectiles_group = pygame.sprite.Group()
player_projectiles_group = pygame.sprite.Group()

player = Player()
game_font = pygame.font.Font(None, 72)
ui_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
restart_button = Button(
    SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
    BUTTON_WIDTH, BUTTON_HEIGHT, "Recomeçar", 40,
    lambda: start_level(1, new_game=True)
)

# --- Funções do Jogo ---
def start_level(level, new_game=False):
    global current_game_state, current_level
    current_level = level
    
    for sprite in all_sprites:
        if sprite != player:
            sprite.kill()
    cars_group.empty()
    enemies_group.empty()
    enemy_projectiles_group.empty()
    player_projectiles_group.empty()
    
    if new_game:
        player.reset_stats()
    else:
        player.reset_position()
        player.reset_ammo()

    if player not in all_sprites:
        all_sprites.add(player)

    # Criação de Carros
    for i, y_pos in enumerate(CAR_LANES_Y):
        direction = 1 if i % 2 == 0 else -1
        num_cars_in_lane = random.randint(2, 3)
        lane_cars_temp = []
        for _ in range(num_cars_in_lane):
            car = Car(y_pos, direction, lane_cars_temp, level=level)
            all_sprites.add(car)
            cars_group.add(car)
            lane_cars_temp.append(car)

    # Lógica de Spawn de Inimigos
    all_safe_zones = []
    all_safe_zones.append(pygame.Rect(0, SCREEN_HEIGHT - SAFE_ZONE_HEIGHT, SCREEN_WIDTH, SAFE_ZONE_HEIGHT))
    for y_pos in CAR_LANES_Y:
        safe_zone_y = y_pos - SAFE_ZONE_HEIGHT
        all_safe_zones.append(pygame.Rect(0, safe_zone_y, SCREEN_WIDTH, SAFE_ZONE_HEIGHT))
    max_y_pos = SCREEN_HEIGHT * ENEMY_SPAWN_TOP_PERCENT
    eligible_zones = [zone for zone in all_safe_zones if zone.top < max_y_pos and zone.top > FINISH_LINE_HEIGHT]
    num_enemies = 1 + (level - 1) // 2
    if num_enemies > 0 and eligible_zones:
        column_width = SCREEN_WIDTH // num_enemies
        horizontal_zones = [pygame.Rect(i * column_width, 0, column_width, SCREEN_HEIGHT) for i in range(num_enemies)]
        random.shuffle(horizontal_zones)
        for i in range(num_enemies):
            horizontal_zone = horizontal_zones[i]
            vertical_zone = random.choice(eligible_zones)
            x = random.randint(horizontal_zone.left + ENEMY_WIDTH, horizontal_zone.right - ENEMY_WIDTH)
            y = vertical_zone.centery
            enemy = Enemy(x, y, all_sprites, enemy_projectiles_group)
            all_sprites.add(enemy)
            enemies_group.add(enemy)

    current_game_state = GAME_STATE_PLAYING

# --- Loop Principal ---
start_level(1, new_game=True)
running = True
while running:
    clock.tick(FPS)

    # Processamento de Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if current_game_state == GAME_STATE_PLAYING:
                if event.key == pygame.K_SPACE:
                    player.shoot(all_sprites, player_projectiles_group)
                if event.key == pygame.K_1:
                    player.select_slot(1)
                if event.key == pygame.K_2:
                    player.select_slot(2)
                if event.key == pygame.K_3:
                    player.select_slot(3)

        if current_game_state in (GAME_STATE_GAME_OVER, GAME_STATE_ALL_CLEARED):
            restart_button.handle_event(event)

    if current_game_state == GAME_STATE_PLAYING:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = PLAYER_SPEED
        player.set_speed(dx, dy)

    # Lógica do Jogo (Update)
    if current_game_state == GAME_STATE_PLAYING:
        # Atualizações
        player.update()
        enemies_group.update()
        enemy_projectiles_group.update()
        player_projectiles_group.update()
        for car_lane_y in CAR_LANES_Y:
            cars_in_this_lane = [car for car in cars_group if car.rect.y == car_lane_y]
            for car in cars_in_this_lane:
                car.update(cars_in_this_lane)

        # Colisões
        pygame.sprite.groupcollide(player_projectiles_group, enemies_group, True, True)
        pygame.sprite.groupcollide(player_projectiles_group, cars_group, True, False)
        pygame.sprite.groupcollide(enemy_projectiles_group, cars_group, True, False)

        hit = False
        if pygame.sprite.spritecollide(player, enemy_projectiles_group, True): hit = True
        if pygame.sprite.spritecollide(player, cars_group, False): hit = True
        if pygame.sprite.spritecollide(player, enemies_group, False): hit = True
        if hit:
            player.lose_life()
            life_lost_feedback_time = pygame.time.get_ticks()

        if player.lives <= 0:
            current_game_state = GAME_STATE_GAME_OVER
        if player.rect.top <= FINISH_LINE_Y:
            if current_level < TOTAL_LEVELS:
                start_level(current_level + 1)
            else:
                current_game_state = GAME_STATE_ALL_CLEARED

    # --- Desenho ---
    screen.fill(BLACK)
    for y_pos in CAR_LANES_Y:
        pygame.draw.rect(screen, DARK_GRAY, [0, y_pos, SCREEN_WIDTH, CAR_HEIGHT])
    pygame.draw.rect(screen, BLUE_FINISH, [0, 0, SCREEN_WIDTH, FINISH_LINE_HEIGHT])
    
    all_sprites.draw(screen)

    # --- UI (MODIFICADA) ---
    if current_game_state == GAME_STATE_PLAYING:
        # UI de Vidas e Fases (cantos superiores)
        level_text = ui_font.render(f"Fase: {current_level}/{TOTAL_LEVELS}", True, WHITE)
        lives_text = ui_font.render(f"Vidas: {player.lives}", True, WHITE)
        screen.blit(level_text, (10, 5))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 5))

        # UI de Munição (topo, centro)
        slot_size = 40 # Diminuído um pouco para caber melhor no topo
        padding = 10
        total_width = (3 * slot_size) + (2 * padding)
        start_x = (SCREEN_WIDTH - total_width) / 2
        start_y = 5 # Posição Y no topo
        
        for i in range(1, 4):
            slot_rect = pygame.Rect(start_x + (i-1)*(slot_size+padding), start_y, slot_size, slot_size)
            border_color = YELLOW if player.selected_slot == i else GRAY
            pygame.draw.rect(screen, border_color, slot_rect, 2)

            slot_key_text = small_font.render(str(i), True, WHITE)
            screen.blit(slot_key_text, (slot_rect.x + 5, slot_rect.y + 2))

            ammo_count = player.ammo.get(i, 0)
            ammo_text = ui_font.render(str(ammo_count), True, WHITE)
            ammo_rect = ammo_text.get_rect(center=slot_rect.center)
            ammo_rect.y += 5
            screen.blit(ammo_text, ammo_rect)

    # Feedback de Dano
    if life_lost_feedback_time > 0 and pygame.time.get_ticks() - life_lost_feedback_time < FLASH_DURATION:
        flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        flash_surface.fill(FLASH_COLOR)
        flash_surface.set_alpha(FLASH_ALPHA)
        screen.blit(flash_surface, (0, 0))

    # Telas de Fim de Jogo
    if current_game_state == GAME_STATE_GAME_OVER:
        text = game_font.render("GAME OVER", True, RED)
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)))
        restart_button.draw(screen)
    elif current_game_state == GAME_STATE_ALL_CLEARED:
        text = game_font.render("VOCÊ VENCEU O JOGO!", True, GREEN)
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)))
        restart_button.draw(screen)
        
    pygame.display.flip()

pygame.quit()
sys.exit()