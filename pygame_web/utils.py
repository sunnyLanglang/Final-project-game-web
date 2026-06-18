# -*- coding: utf-8 -*-
# utils.py
import pygame
from pygame.locals import *   
from constants import *

def load_font(size):
    font_names = ["Arial", "Times New Roman", "Segoe UI", "Tahoma", "Verdana"]
    for name in font_names:
        try:
            font = pygame.font.SysFont(name, size)
            if font.render("А", True, (255,255,255)).get_width() > 0:
                print(f"使用系统字体: {name}")
                return font
        except:
            continue
    try:
        font = pygame.font.Font("simhei.ttf", size)
        print("使用 simhei.ttf")
        return font
    except:
        try:
            font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", size)
            print("使用 simhei.ttf (系统目录)")
            return font
        except:
            print("警告: 未找到字体，使用默认")
            return pygame.font.Font(None, size)

def wrap_text(text, font, max_width):
    """将文本按空格分行，若单个单词过长则按字符数截断"""
    words = text.split(' ')
    lines = []
    cur = []
    for w in words:
        test = ' '.join(cur + [w])
        if font.size(test)[0] <= max_width:
            cur.append(w)
        else:
            if cur:
                lines.append(' '.join(cur))
                cur = [w]
            else:
                avg_char_width = font.size('А')[0] if font.size('А')[0] > 0 else 18
                chars_per_line = max(1, max_width // avg_char_width)
                for i in range(0, len(w), chars_per_line):
                    lines.append(w[i:i+chars_per_line])
                cur = []
    if cur:
        lines.append(' '.join(cur))
    return lines if lines else [text]

class Button:
    def __init__(self, x, y, w, h, text, font, color=BLUE, text_color=WHITE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, screen):
        color = (self.color[0]//2, self.color[1]//2, self.color[2]//2) if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class MultiLineButton:
    def __init__(self, x, y, max_width, lines, font, color=BLUE, text_color=WHITE):
        self.x = x
        self.y = y
        self.max_width = max_width
        self.lines = lines
        self.font = font
        self.color = color
        self.text_color = text_color
        self.is_hovered = False
        self.line_height = font.get_linesize()
        self.height = len(lines) * self.line_height + 10
        self.rect = pygame.Rect(x, y, max_width, self.height)
        self.opt_index = None
        self.opt_data = None

    def draw(self, screen):
        color = (self.color[0]//2, self.color[1]//2, self.color[2]//2) if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8)
        for i, line in enumerate(self.lines):
            surf = self.font.render(line, True, self.text_color)
            text_rect = surf.get_rect(center=(self.x + self.max_width//2, self.y + 5 + i*self.line_height + self.line_height//2))
            screen.blit(surf, text_rect)

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False