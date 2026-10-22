"""Read-only unit guide; the controller pauses the match while it is open."""
import pygame

import config as C
from ui import load_font
from art import fruit_image, character_image


class FieldGuide:
    button_rect = pygame.Rect(485, C.SCREEN_H - 42, 295, 32)
    close_rect = pygame.Rect(642, 28, 125, 36)

    def __init__(self):
        self.font = load_font(17)
        self.title_font = load_font(25)

    def text(self, surface, value, pos, title=False, color=(40, 57, 38)):
        surface.blit((self.title_font if title else self.font).render(value, True, color), pos)

    def draw_button(self, surface):
        pygame.draw.rect(surface, (46, 76, 47), self.button_rect, border_radius=8)
        self.text(surface, '防御塔与怪物图鉴  [I]', (505, C.SCREEN_H - 37), color=(255, 240, 195))

    def draw(self, surface):
        surface.fill((240, 235, 213))
        pygame.draw.rect(surface, (170, 153, 104), surface.get_rect().inflate(-24, -24), 2, border_radius=14)
        self.text(surface, '防守手册', (30, 25), True)
        pygame.draw.rect(surface, (215, 205, 175), self.close_rect, border_radius=6)
        self.text(surface, '返回 [I / Esc]', (650, 36))
        self.text(surface, '查看期间战斗暂停；积分来自击杀，建塔不会扣除积分。', (30, 72))
        self.text(surface, '防御塔', (30, 109), True)
        for i, kind in enumerate(C.SHOP_ORDER):
            spec = C.FRUITS[kind]
            y = 151 + i * 59
            sprite = fruit_image(kind, 36)
            surface.blit(sprite, sprite.get_rect(center=(47, y + 17)))
            self.text(surface, f"{spec['label']}  ·  攻击 {spec['damage']}  ·  价格 {spec['cost']}  ·  生命 {spec['hp']}", (75, y))
            ability = '范围伤害' if kind == 'melon' else '单体攻击'
            self.text(surface, f"{ability}；每 {spec['interval']:g} 秒攻击，射程 {spec['rng']:g} 格", (75, y + 25))
        self.text(surface, '来袭怪物', (30, 334), True)
        for i, (kind, spec) in enumerate(C.MONSTERS.items()):
            y = 379 + i * 58
            sprite = character_image(kind, 38)
            if sprite is not None:
                surface.blit(sprite, sprite.get_rect(center=(47, y + 17)))
            else:
                pygame.draw.circle(surface, spec['color'], (47, y + 17), 13)
            self.text(surface, f"{spec['label']}  ·  生命 {spec['hp']}  ·  速度 {spec['speed']:g} 格/秒", (75, y))
            detail = f"到达终点扣 {spec['bite']} 血；击杀获得 {spec['reward']} 金币和积分"
            if kind == 'thrower':
                detail += f"；投石伤害 {spec['throw_damage']}"
            self.text(surface, detail, (75, y + 25))
        self.text(surface, '操作：1–3或点击卡片选塔，左键建塔；P 暂停，Enter 继续。', (30, 628))
