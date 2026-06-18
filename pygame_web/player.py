# -*- coding: utf-8 -*-
# player.py
import pygame
from constants import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.max_hp = 100
        self.hp = 100
        self.max_sp = 100
        self.sp = 100
        self.color = BLUE

    def take_damage(self, hp_amount=0, sp_amount=0):
        self.hp = max(0, self.hp - hp_amount)
        self.sp = max(0, self.sp - sp_amount)

    def heal(self, hp_amount=0, sp_amount=0):
        self.hp = min(self.max_hp, self.hp + hp_amount)
        self.sp = min(self.max_sp, self.sp + sp_amount)

    def is_alive(self):
        return self.hp > 0

    def move_right(self, amount):
        new_x = self.x + amount
        if new_x > END_X:
            new_x = END_X
        self.x = new_x

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        if -self.width < screen_x < SCREEN_WIDTH:
            pygame.draw.rect(screen, self.color, (screen_x, self.y, self.width, self.height))
            pygame.draw.circle(screen, WHITE, (screen_x + 8, self.y + 12), 5)
            pygame.draw.circle(screen, WHITE, (screen_x + 22, self.y + 12), 5)
            pygame.draw.circle(screen, BLACK, (screen_x + 8, self.y + 12), 2)
            pygame.draw.circle(screen, BLACK, (screen_x + 22, self.y + 12), 2)

    def draw_status_bars(self, screen, font):
        bar_width = 200
        bar_height = 20
        pygame.draw.rect(screen, DARK_GRAY, (20, 20, bar_width, bar_height))
        hp_width = int(bar_width * (self.hp / self.max_hp))
        pygame.draw.rect(screen, RED, (20, 20, hp_width, bar_height))
        hp_text = font.render(f"HP {self.hp}/{self.max_hp}", True, WHITE)
        screen.blit(hp_text, (20, 5))
        pygame.draw.rect(screen, DARK_GRAY, (20, 55, bar_width, bar_height))
        sp_width = int(bar_width * (self.sp / self.max_sp))
        pygame.draw.rect(screen, GREEN, (20, 55, sp_width, bar_height))
        sp_text = font.render(f"SP {self.sp}/{self.max_sp}", True, WHITE)
        screen.blit(sp_text, (20, 40))