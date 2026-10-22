"""Two-page unit guide; opening it freezes the entire simulation."""
import pygame
import config as C
from ui import load_font
from art import fruit_image, character_image


class FieldGuide:
    button_rect = pygame.Rect(650, C.HUD_H + C.FIELD_H + 4, 130, 28)
    close_rect = pygame.Rect(642, 28, 125, 36)
    towers_rect = pygame.Rect(28, 84, 170, 34)
    monsters_rect = pygame.Rect(210, 84, 170, 34)

    def __init__(self):
        self.font = load_font(16)
        self.title_font = load_font(24)
        self.tab = 'towers'

    def text(self, surface, value, pos, title=False, color=(40, 57, 38)):
        surface.blit((self.title_font if title else self.font).render(value, True, color), pos)

    def draw_button(self, surface):
        pygame.draw.rect(surface, (46, 76, 47), self.button_rect, border_radius=8)
        self.text(surface, '图鉴 [I]', (683, self.button_rect.y + 3), color=(255, 240, 195))

    def draw(self, surface):
        surface.fill((240, 235, 213))
        self.text(surface, '防守手册', (28, 26), True)
        pygame.draw.rect(surface, (215, 205, 175), self.close_rect, border_radius=6)
        self.text(surface, '返回 [I / Esc]', (650, 36))
        for rect, label, tab in ((self.towers_rect, '八种防御塔', 'towers'), (self.monsters_rect, '八类怪物', 'monsters')):
            pygame.draw.rect(surface, (186, 203, 137) if self.tab == tab else (218, 215, 184), rect, border_radius=7)
            self.text(surface, label, (rect.x + 18, rect.y + 6))
        self.text(surface, 'Tab 切换；查看时暂停。下列为一级 / 基础值，后关怪物逐步增强。', (28, 127))
        items = list(C.SHOP_ORDER) if self.tab == 'towers' else list(C.MONSTERS)
        for i, kind in enumerate(items):
            x, y = 28 + i % 2 * 390, 165 + i // 2 * 128
            pygame.draw.rect(surface, (250, 246, 226), (x, y, 365, 115), border_radius=10)
            sprite = fruit_image(kind, 58) if self.tab == 'towers' else character_image(kind, 64)
            if sprite:
                surface.blit(sprite, sprite.get_rect(center=(x + 37, y + 43)))
            spec = C.FRUITS[kind] if self.tab == 'towers' else C.MONSTERS[kind]
            self.text(surface, spec['label'], (x + 77, y + 8))
            if self.tab == 'towers':
                self.text(surface, f"{spec['role']} · 攻击{spec['damage']} · {spec['cost']}金币", (x + 77, y + 33))
                self.text(surface, f"间隔{spec['interval']:g}秒 · 射程{spec['rng']:g}格", (x + 77, y + 58))
                self.text(surface, f"第{spec['unlock']}关开放，最高三级", (x + 16, y + 88))
            else:
                self.text(surface, f"生命{spec['hp']} · 速度{spec['speed']:g}格/秒", (x + 77, y + 33))
                self.text(surface, f"击杀获得{spec['reward']}金币和积分", (x + 77, y + 58))
                debut = next(n + 1 for n, level in enumerate(C.LEVELS) if kind in level['monsters'])
                self.text(surface, f"第{debut}关出现 · 每只漏怪扣1血", (x + 16, y + 88))
        self.text(surface, '点击已建炮塔 → 升级 / 出售；萝卜保持3血，第三只漏怪失败。', (28, 699))
