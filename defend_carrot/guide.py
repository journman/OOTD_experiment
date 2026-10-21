"""Read-only unit guide; the controller pauses the match while it is open."""
import os

import pygame

import config as C


class FieldGuide:
    button_rect = pygame.Rect(485, C.SCREEN_H - 70, 295, 45)
    close_rect = pygame.Rect(642, 28, 125, 36)

    def __init__(self):
        path = next((p for p in (r'C:\Windows\Fonts\msyh.ttc',
                                r'C:\Windows\Fonts\simhei.ttf',
                                '/System/Library/Fonts/PingFang.ttc',
                                '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
                     if os.path.exists(p)), None)
        self.font = pygame.font.Font(path, 17)
        self.title_font = pygame.font.Font(path, 25)

    def text(self, surface, value, pos, title=False, color=(40, 57, 38)):
        surface.blit((self.title_font if title else self.font).render(value, True, color), pos)

    def draw_button(self, surface):
        pygame.draw.rect(surface, (46, 76, 47), self.button_rect, border_radius=8)
        self.text(surface, '水果与怪物图鉴  [I]', (505, C.SCREEN_H - 59), color=(255, 240, 195))

    def draw(self, surface):
        surface.fill((240, 235, 213))
        self.text(surface, '防守手册', (30, 25), True)
        pygame.draw.rect(surface, (215, 205, 175), self.close_rect, border_radius=6)
        self.text(surface, '返回 [I / Esc]', (650, 36))
        self.text(surface, '查看期间战斗暂停；积分来自击杀，建塔不会扣除积分。', (30, 72))
        self.text(surface, '水果防御塔', (30, 109), True)
        fruit_names = {'apple': '苹果', 'orange': '橙子', 'melon': '西瓜'}
        for i, kind in enumerate(C.SHOP_ORDER):
            spec = C.FRUITS[kind]
            y = 151 + i * 59
            pygame.draw.circle(surface, spec['color'], (47, y + 17), 13)
            self.text(surface, f"{fruit_names[kind]}  ·  攻击 {spec['damage']}  ·  价格 {spec['cost']}  ·  生命 {spec['hp']}", (75, y))
            ability = '范围伤害' if kind == 'melon' else '单体攻击'
            self.text(surface, f"{ability}；每 {spec['interval']:g} 秒攻击，射程 {spec['rng']:g} 格", (75, y + 25))
        self.text(surface, '来袭怪物', (30, 334), True)
        names = {'slime': '史莱姆', 'bat': '蝙蝠', 'golem': '石巨人', 'thrower': '投石怪'}
        for i, (kind, spec) in enumerate(C.MONSTERS.items()):
            y = 379 + i * 58
            pygame.draw.circle(surface, spec['color'], (47, y + 17), 13)
            self.text(surface, f"{names[kind]}  ·  生命 {spec['hp']}  ·  速度 {spec['speed']:g} 格/秒", (75, y))
            detail = f"到达终点扣 {spec['bite']} 血；击杀获得 {spec['reward']} 金币和积分"
            if kind == 'thrower':
                detail += f"；投石伤害 {spec['throw_damage']}"
            self.text(surface, detail, (75, y + 25))
        self.text(surface, '操作：1–3 选择水果，左键建塔，右键取消；胜负后 R 重开。', (30, 628))
