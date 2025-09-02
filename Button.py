# Button.py

import pygame
from Settings import *

class Button:
    def __init__(self, x, y, width, height, text, font_size, action):
        # ... (código idêntico ao anterior)
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        
        self.font = pygame.font.Font(None, font_size)
        self.base_color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.current_color = self.base_color
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        
        text_surface = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.base_color
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.action()