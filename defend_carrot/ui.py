"""Chinese typography and menu/pause/result screens for the fruit defense game."""
import os

import pygame

import config as C


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


class GameUI:
    primary_rect = pygame.Rect(245, 375, 310, 52)
    secondary_rect = pygame.Rect(245, 445, 310, 47)
    pause_rect = pygame.Rect(485, C.SCREEN_H - 80, 295, 32)

    def __init__(self, game):
        self.game = game
        self.fonts = {size: load_font(size) for size in (15, 18, 22, 38)}

    def text(self, value, center, size=18, color=(245, 235, 204)):
        image = self.fonts[size].render(value, True, color)
        self.game.screen.blit(image, image.get_rect(center=center))

    def button(self, rect, label):
        screen = self.game.screen
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (89, 132, 70) if hovered else (63, 102, 55), rect, border_radius=10)
        pygame.draw.rect(screen, (191, 187, 122), rect, 2, border_radius=10)
        self.text(label, rect.center, 22)

    def draw_overlay(self):
        g = self.game
        overlay = pygame.Surface(g.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((10, 24, 18, 185))
        g.screen.blit(overlay, (0, 0))
        panel = pygame.Rect(125, 115, 550, 440)
        pygame.draw.rect(g.screen, (33, 59, 42), panel, border_radius=20)
        pygame.draw.rect(g.screen, (173, 166, 103), panel, 3, border_radius=20)
        titles = {'menu': '保卫萝卜 · 水果防线', 'paused': '休息一下，防线已暂停',
                  'levelclear': '花园守住了！', 'won': '两关通关，守护成功！', 'lost': '萝卜失守了'}
        self.text(titles[g.state], (400, 174), 38)
        if g.state == 'menu':
            lines = ('两张地图 · 三种水果 · 四类来袭怪物',
                     '1–3 或点击卡片选塔，左键建造，右键取消',
                     '击杀获得金币与积分，漏怪只扣萝卜生命',
                     'I 查看图鉴，P 暂停；Esc 暂停或返回菜单')
            primary, secondary = '开始挑战  [Enter]', '水果与怪物图鉴  [I]'
        else:
            lines = (C.LEVELS[g.level_index]['name'],
                     f'累计积分 {g.score}    击杀 {g.kills}    金币 {g.coins}',
                     f'萝卜生命 {max(0, g.carrot.hp):g}/{C.CARROT_HP}    用时 {g.elapsed:.1f} 秒',
                     '下一关回收存活防御塔原价，萝卜恢复生命' if g.state == 'levelclear'
                     else '查看图鉴不会改变挑战进度')
            primary = ('继续防守  [P / Enter]' if g.state == 'paused' else
                       '前往第二关  [Enter]' if g.state == 'levelclear' else '重新挑战  [R / Enter]')
            secondary = '结束本次挑战，返回菜单' if g.state == 'paused' else '返回主菜单  [Esc]'
        for i, line in enumerate(lines):
            self.text(line, (400, 235 + i * 31), 18)
        self.button(self.primary_rect, primary)
        self.button(self.secondary_rect, secondary)
        self.text('主菜单按 Esc 退出游戏', (400, 526), 15, (186, 196, 162))
