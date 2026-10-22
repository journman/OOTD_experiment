"""Chinese typography and menu/pause/result screens for the fruit defense game."""
import os
import math
from functools import lru_cache

import pygame

import config as C
from art import fruit_image, character_image
from entities import tile_center


def load_font(size):
    for path in (r'C:\Windows\Fonts\msyh.ttc', r'C:\Windows\Fonts\simhei.ttf',
                 '/System/Library/Fonts/PingFang.ttc',
                 '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'):
        if os.path.exists(path):
            try:
                return pygame.font.Font(path, size)
            except (OSError, pygame.error):
                continue
    return pygame.font.Font(None, size)


@lru_cache(maxsize=8)
def panel_background(size, dark=False):
    image = pygame.Surface(size)
    top, bottom = ((48, 80, 57), (27, 54, 40)) if dark else ((249, 242, 215), (220, 206, 163))
    for y in range(size[1]):
        t = y / max(1, size[1] - 1)
        color = tuple(round(a + (b - a) * t) for a, b in zip(top, bottom))
        pygame.draw.line(image, color, (0, y), (size[0], y))
    pygame.draw.line(image, (181, 159, 93), (0, 0), (size[0], 0), 2)
    return image


class GameUI:
    primary_rect = pygame.Rect(245, 365, 310, 48)
    secondary_rect = pygame.Rect(245, 425, 310, 42)
    level_button_rect = pygame.Rect(245, 480, 310, 40)
    pause_rect = pygame.Rect(520, C.HUD_H + C.FIELD_H + 4, 120, 28)
    speed_rect = pygame.Rect(650, C.HUD_H + C.FIELD_H + 40, 130, 28)
    upgrade_rect = pygame.Rect(520, C.HUD_H + C.FIELD_H + 128, 125, 32)
    sell_rect = pygame.Rect(655, C.HUD_H + C.FIELD_H + 128, 125, 32)

    def __init__(self, game):
        self.game = game
        self.fonts = {size: load_font(size) for size in (13, 15, 18, 22, 38)}

    def text(self, value, center, size=18, color=(245, 235, 204)):
        image = self.fonts[size].render(value, True, color)
        self.game.screen.blit(image, image.get_rect(center=center))

    def button(self, rect, label):
        screen = self.game.screen
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (89, 132, 70) if hovered else (63, 102, 55), rect, border_radius=10)
        pygame.draw.rect(screen, (191, 187, 122), rect, 2, border_radius=10)
        self.text(label, rect.center, 15 if rect.h < 40 else 22)

    def draw_shop(self):
        g = self.game
        base = C.SCREEN_H - C.SHOP_H
        g.screen.blit(panel_background((C.SCREEN_W, C.SHOP_H)), (0, base))
        for i, kind in enumerate(C.SHOP_ORDER):
            spec, rect = C.FRUITS[kind], g._card_rect(i)
            opened = kind in g.available_towers
            selected = g.selected == kind
            affordable = opened and g.coins >= spec['cost']
            color = (255, 243, 184) if selected else (255, 251, 232) if affordable else (218, 218, 201)
            pygame.draw.rect(g.screen, color, rect, border_radius=8)
            pygame.draw.rect(g.screen, (195, 145, 46) if selected else (153, 155, 109), rect, 2, border_radius=8)
            sprite = fruit_image(kind, 46)
            if not affordable:
                sprite = pygame.transform.grayscale(sprite)
            g.screen.blit(sprite, sprite.get_rect(center=(rect.x + 23, rect.y + 30)))
            for value, y in ((spec['label'], 3),
                             (f"{spec['cost']}金币" if opened else f"第{spec['unlock']}关开放", 22),
                             (spec['role'], 39)):
                text = self.fonts[13].render(value, True, (44, 70, 40) if opened else (111, 114, 98))
                g.screen.blit(text, (rect.x + 45, rect.y + y))
            self.text(str(i + 1), (rect.x + 8, rect.y + 8), 13, (74, 104, 51))
        self.button(self.speed_rect, f'速度 {g.speed_multiplier}倍 [Tab]')
        tower = g.inspected if g.inspected and g.inspected.alive else None
        if tower:
            self.text(f'{tower.label}  {tower.level}级', (580, base + 54), 15, (44, 70, 40))
            self.text(f'伤害{tower.damage:g}  射程{tower.rng / C.TILE:.1f}格', (650, base + 87), 15, (64, 80, 46))
            self.text(f'每{tower.interval:.2f}秒攻击', (650, base + 109), 13, (94, 103, 65))
            self.button(self.upgrade_rect, f'升级 {tower.upgrade_cost} [U]' if tower.upgrade_cost else '已满三级')
            self.button(self.sell_rect, f'出售 {tower.sell_value}')
        else:
            self.text(f'本关开放 {len(g.available_towers)} / 8 种塔', (580, base + 54), 13, (44, 70, 40))
            self.text('点击场上防御塔，可升级或出售', (650, base + 99), 15, (64, 80, 46))
            self.text(C.LEVELS[g.level_index]['hint'], (650, base + 132), 15, (120, 95, 37))

    def draw_hud(self):
        g = self.game
        g.screen.blit(panel_background((C.SCREEN_W, C.HUD_H), True), (0, 0))
        pygame.draw.rect(g.screen, (31, 57, 40), (9, 7, 155, 42), border_radius=10)
        pygame.draw.circle(g.screen, (165, 113, 34), (32, 28), 14)
        pygame.draw.circle(g.screen, (244, 198, 72), (32, 26), 12)
        pygame.draw.circle(g.screen, (255, 228, 135), (32, 26), 8, 2)
        self.text('金币', (82, 17), 13, (225, 224, 177))
        self.text(str(g.coins), (90, 35), 22, (255, 225, 131))
        level = C.LEVELS[g.level_index]
        image = self.fonts[18].render(level['name'], True, (247, 242, 209))
        g.screen.blit(image, (183, 5))
        self.text(f"第 {min(g.wave_index + 1, len(level['waves']))}/{len(level['waves'])} 波", (534, 19), 15)
        detail = self.fonts[13].render(f'击杀 {g.kills}    积分 {g.score}', True, (196, 216, 173))
        g.screen.blit(detail, (184, 33))
        self.text(f'萝卜生命 {max(0, g.carrot.hp):g}/{C.CARROT_HP}', (693, 13), 13)
        rect = pygame.Rect(605, 28, 176, 15)
        pygame.draw.rect(g.screen, (20, 38, 28), rect.inflate(4, 4), border_radius=8)
        color = ((160, 203, 101) if g.carrot.hp == 3 else
                 (239, 187, 75) if g.carrot.hp == 2 else (237, 117, 94))
        for i in range(C.CARROT_HP):
            left = rect.x + round(i * rect.w / C.CARROT_HP)
            right = rect.x + round((i + 1) * rect.w / C.CARROT_HP)
            slot = pygame.Rect(left + 1, rect.y, right - left - 3, rect.h)
            filled = i < g.carrot.hp
            pygame.draw.rect(g.screen, color if filled else (59, 77, 55), slot, border_radius=4)
            if filled:
                pygame.draw.line(g.screen, (255, 235, 174),
                                 (slot.x + 3, slot.y + 3), (slot.right - 4, slot.y + 3), 2)

    def draw_placement(self, pos=None):
        g = self.game
        cell = g.field_cell(pygame.mouse.get_pos() if pos is None else pos)
        tower = g.inspected if g.inspected and g.inspected.alive else (g.fruit_at(*cell) if cell else None)
        if g.selected and cell is None or not g.selected and tower is None:
            return
        if not g.selected:
            cell = tower.col, tower.row
        col, row = cell
        kind = g.selected or tower.kind
        valid = not g.building_error(cell) if g.selected else True
        color = (127, 235, 149) if valid else (255, 121, 101)
        x, y = tile_center(col, row)
        y -= C.HUD_H
        overlay = pygame.Surface((C.FIELD_W, C.FIELD_H), pygame.SRCALPHA)
        radius = round(C.FRUITS[kind]['rng'] * C.TILE if g.selected else tower.rng)
        pygame.draw.circle(overlay, (*color, 32), (x, y), radius)
        pygame.draw.circle(overlay, (*color, 170), (x, y), radius, 2)
        rect = pygame.Rect(col * C.TILE, row * C.TILE, C.TILE, C.TILE)
        pygame.draw.rect(overlay, (*color, 55), rect, border_radius=5)
        pygame.draw.rect(overlay, (*color, 230), rect, 2, border_radius=5)
        if g.selected:
            ghost = fruit_image(kind, C.TOWER_SPRITE_SIZE).copy()
            ghost.set_alpha(150)
            overlay.blit(ghost, ghost.get_rect(center=(x, y)))
        g.screen.blit(overlay, (0, C.HUD_H))

    def draw_battle_info(self, pos=None):
        g = self.game
        if g.notice_timer > 0:
            message = g.notice
        elif g.selected:
            cell = g.field_cell(pygame.mouse.get_pos() if pos is None else pos)
            reason = g.building_error(cell) if cell else "移动到草地查看射程，右键取消"
            message = f"{C.FRUITS[g.selected]['label']} · {reason or '可建造，左键确认'}"
        elif g.wave_timer < 0:
            message = f"下一波还有 {math.ceil(-g.wave_timer)} 秒 · 提前布置防线"
        else:
            message = f"{C.LEVELS[g.level_index]['wave_labels'][g.wave_index]} · 场上 {len(g.monsters)} 只 · 点击炮塔升级"
        # The last map row remains unobstructed; feedback sits above the cards.
        panel = pygame.Surface((500, 25), pygame.SRCALPHA)
        panel.fill((44, 68, 45, 230))
        g.screen.blit(panel, (10, C.SCREEN_H - C.SHOP_H + 4))
        self.text(message, (260, C.SCREEN_H - C.SHOP_H + 16), 13,
                  (255, 218, 145) if g.notice_timer > 0 else (235, 244, 211))

    def draw_overlay(self):
        g = self.game
        overlay = pygame.Surface(g.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((10, 24, 18, 185))
        g.screen.blit(overlay, (0, 0))
        panel = pygame.Rect(125, 115, 550, 440)
        pygame.draw.rect(g.screen, (12, 28, 17), panel.move(0, 8), border_radius=20)
        pygame.draw.rect(g.screen, (245, 237, 205), panel, border_radius=20)
        pygame.draw.rect(g.screen, (175, 150, 82), panel, 3, border_radius=20)
        for i, kind in enumerate(('apple', 'orange', 'melon')):
            sprite = fruit_image(kind, 28)
            g.screen.blit(sprite, sprite.get_rect(center=(367 + i * 33, 138)))
        titles = {'menu': C.TITLE, 'paused': '休息一下，防线已暂停',
                  'levelclear': '本关守住了！', 'won': '八关通关，守护成功！', 'lost': '萝卜失守了'}
        self.text(titles[g.state], (400, 181), 38, (43, 77, 44))
        if g.state == 'menu':
            lines = ('八张地图 · 八种炮塔 · 三大主题',
                     '1–8 选塔；点击场上炮塔升级或出售',
                     '萝卜只有 3 血，每漏过一只怪物扣 1 血',
                     '关卡逐步解锁，通关进度自动保存在本地')
            primary, secondary = f"继续第{g.progress['unlocked']}关 [Enter]", '防御塔与怪物图鉴  [I]'
            self.button(self.level_button_rect, '选择关卡 / 重玩 [L]')
        else:
            lines = (C.LEVELS[g.level_index]['name'],
                     f'累计积分 {g.score}    击杀 {g.kills}    金币 {g.coins}',
                     f'萝卜生命 {max(0, g.carrot.hp):g}/{C.CARROT_HP}    用时 {g.elapsed:.1f} 秒',
                     '下一关使用独立开局金币，萝卜恢复3血' if g.state == 'levelclear'
                     else '查看图鉴不会改变挑战进度')
            primary = ('继续防守  [P / Enter]' if g.state == 'paused' else
                       f'前往第{g.level_index + 2}关 [Enter]' if g.state == 'levelclear' else '重新挑战  [R / Enter]')
            secondary = '结束本次挑战，返回菜单' if g.state == 'paused' else '返回主菜单  [Esc]'
        for i, line in enumerate(lines):
            self.text(line, (400, 235 + i * 31), 18, (67, 84, 55))
        self.button(self.primary_rect, primary)
        self.button(self.secondary_rect, secondary)
        footnote = ('通关进度暂未写入，请检查存档目录权限' if g.save_error and g.state in ('levelclear', 'won')
                    else '主菜单按 Esc 退出游戏')
        self.text(footnote, (400, 539), 15, (105, 112, 77))

    @staticmethod
    def level_rect(index):
        return pygame.Rect(25 + index % 4 * 190, 200 + index // 4 * 165, 175, 140)

    def draw_level_select(self):
        g = self.game
        g.screen.fill((232, 231, 199))
        self.text('冒险地图 · 天际 / 丛林 / 沙漠', (400, 85), 22, (49, 86, 49))
        self.text('通关开放下一关；金色标记代表满血通关', (400, 131), 18, (90, 104, 62))
        for i, level in enumerate(C.LEVELS):
            rect = self.level_rect(i)
            opened = i < g.progress['unlocked']
            pygame.draw.rect(g.screen, (255, 247, 209) if opened else (186, 192, 169), rect, border_radius=14)
            pygame.draw.rect(g.screen, (169, 139, 52) if g.progress['best'].get(str(i)) == 3 else (112, 143, 84), rect, 2, border_radius=14)
            self.text(level['name'].split(' · ')[-1], (rect.centerx, rect.y + 30), 18, (50, 80, 44))
            self.text(f"{len(level['waves'])}波 · {len(level['towers'])}种塔", (rect.centerx, rect.y + 65), 15, (85, 97, 57))
            best = g.progress['best'].get(str(i))
            label = f'最佳剩余 {best}/3 血' if best else f"开局 {level['start_coins']} 金币" if opened else '通关前一关解锁'
            self.text(label, (rect.centerx, rect.y + 99), 13, (127, 103, 38))
        self.text('点击已开放的关卡出发；Esc / L 返回主菜单', (400, 600), 18, (69, 95, 52))
