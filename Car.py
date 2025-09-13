# Car.py

import pygame
import random
from Settings import *

class Car(pygame.sprite.Sprite):
    def __init__(self, y_pos, direction, all_cars_in_lane, level):
        super().__init__()
        # Carrega as imagens dos carros apenas uma vez (classe)
        if not hasattr(Car, 'car_images'):
            Car.car_images = []
            for i in range(1, 7):
                img = pygame.image.load(f"assets/car{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (CAR_HEIGHT, CAR_WIDTH))
                img = pygame.transform.rotate(img, -90)
                Car.car_images.append(img)

        self.direction = direction
        # Escolhe uma imagem aleatória para este carro e rotaciona conforme a direção
        base_img = random.choice(Car.car_images)
        if self.direction == 1:
            self.image = pygame.transform.rotate(base_img, 0)  # Para a direita
        else:
            self.image = pygame.transform.rotate(base_img, 180)  # Para a esquerda
        self.rect = self.image.get_rect()
        self.rect.y = y_pos

        min_speed = CAR_BASE_SPEED_MIN + (level - 1) * CAR_SPEED_INCREMENT
        max_speed = CAR_BASE_SPEED_MAX + (level - 1) * CAR_SPEED_INCREMENT
        
        # MODIFICADO: Armazena a velocidade original e a velocidade atual separadamente
        self.original_speed = random.uniform(min_speed, max_speed)
        self.speed = self.original_speed

        self._initial_placement(all_cars_in_lane)

    def _initial_placement(self, all_cars_in_lane):
        # ... (esta função permanece exatamente a mesma)
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            if self.direction == 1:
                self.rect.x = random.randint(-SCREEN_WIDTH, -CAR_WIDTH) 
            else:
                self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)

            overlap = False
            for other_car in all_cars_in_lane:
                if other_car != self:
                    self_check_rect = self.rect.inflate(CAR_SPAWN_OFFSET, 0)
                    if self_check_rect.colliderect(other_car.rect):
                        overlap = True
                        break
            
            if not overlap:
                placed = True
            attempts += 1
        
        if not placed:
            if self.direction == 1:
                self.rect.x = -CAR_WIDTH 
            else:
                self.rect.x = SCREEN_WIDTH

    # MODIFICADO: Lógica de atualização completamente refeita
    def update(self, all_cars_in_lane):
        """Move o carro, ajustando a velocidade para evitar colisões na pista."""
        
        # --- LÓGICA ANTI-COLISÃO ---
        leading_car = None
        min_distance = float('inf')

        # Encontra o carro mais próximo diretamente à frente
        for other_car in all_cars_in_lane:
            if other_car is self:
                continue

            # Se estiver se movendo para a direita
            if self.direction == 1:
                distance = other_car.rect.left - self.rect.right
                if 0 < distance < min_distance:
                    min_distance = distance
                    leading_car = other_car
            
            # Se estiver se movendo para a esquerda
            elif self.direction == -1:
                distance = self.rect.left - other_car.rect.right
                if 0 < distance < min_distance:
                    min_distance = distance
                    leading_car = other_car
        
        # Se houver um carro à frente e estiver muito perto, reduza a velocidade
        if leading_car and min_distance < CAR_SAFETY_DISTANCE:
            # A velocidade do carro de trás não deve exceder a do carro da frente
            self.speed = min(self.original_speed, leading_car.speed)
        else:
            # Se não houver perigo, volte à velocidade normal
            self.speed = self.original_speed

        # --- MOVIMENTO E REPOSICIONAMENTO ---
        self.rect.x += self.speed * self.direction
        
        repositioned = False
        if self.direction == 1 and self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
            repositioned = True
        elif self.direction == -1 and self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
            repositioned = True

        if repositioned:
            # A lógica para evitar sobreposição ao reaparecer ainda é útil
            self._initial_placement(all_cars_in_lane)