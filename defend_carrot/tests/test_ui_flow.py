"""Real event coverage for menus, pause, map transitions and settlements."""
import os
from pathlib import Path
import sys

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pygame
import config as C
from game import Game
from entities import Apple, tile_center


def main():
    g = Game()
    try:
        def key(value):
            g.handle_event(pygame.event.Event(pygame.KEYDOWN, key=value))

        def click(rect):
            g.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center))

        def snapshot():
            return (g.elapsed, g.wave_timer, g.coins, g.score, len(g.monsters), len(g.fruits))

        assert g.state == 'menu'
        before = snapshot()
        g.update(60)
        key(pygame.K_1)
        assert g.selected is None and snapshot() == before
        click(g.ui.secondary_rect)
        assert g.guide_open and g.state == 'menu'
        key(pygame.K_ESCAPE)
        assert not g.guide_open and g.state == 'menu'
        g.draw()
        click(g.ui.primary_rect)
        assert g.state == 'playing'
        click(g._card_rect(0))
        assert g.selected == C.SHOP_ORDER[0]
        key(pygame.K_ESCAPE)
        assert g.state == 'paused'
        before = snapshot()
        key(pygame.K_3)
        g.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=3, pos=(100, 100)))
        g.update(30)
        assert snapshot() == before and g.selected == C.SHOP_ORDER[0]
        g.draw()
        key(pygame.K_i)
        key(pygame.K_ESCAPE)
        assert g.state == 'paused' and not g.guide_open
        click(g.ui.primary_rect)
        assert g.state == 'playing'
        click(g.ui.pause_rect)
        assert g.state == 'paused'
        key(pygame.K_p)
        assert g.state == 'playing'

        first_path = list(g.path)
        first_cells = set(g.path_cells)
        g.fruits = [Apple(4, 1), Apple(9, 1)]
        g.fruits[-1].alive = False
        g.score, g.kills, g.coins = 77, 5, 123
        g.wave_index = len(C.LEVELS[0]['waves']) - 1
        g.spawn_queue = []
        g.update(1 / 60)
        assert g.state == 'levelclear' and g.level_index == 0
        g.draw()
        before = snapshot()
        # Arbitrary clicks must not restart the campaign.
        g.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(0, 0)))
        g.update(30)
        assert snapshot() == before and g.state == 'levelclear'
        key(pygame.K_RETURN)
        assert g.level_index == 1 and g.state == 'playing'
        assert g.path != first_path and g.path_cells != first_cells
        assert g.coins == 123 + C.FRUITS['apple']['cost'] + C.PASSIVE_INCOME
        assert (g.score, g.kills, g.carrot.hp) == (77, 5, C.CARROT_HP)
        assert not any((g.fruits, g.monsters, g.bullets, g.rocks, g.effects))
        assert (g.carrot.x, g.carrot.y) == tile_center(*C.LEVELS[1]['path'][-1])
        for col, row in g.path_cells:
            if 0 <= col < C.GRID_COLS and 0 <= row < C.GRID_ROWS:
                assert not g.can_build(col, row)
        g.draw()
        g.wave_index = len(C.LEVELS[1]['waves']) - 1
        g.spawn_queue = []
        g._check_victory()
        assert g.state == 'won'
        g.draw()
        click(g.ui.secondary_rect)
        assert g.state == 'menu'
        key(pygame.K_RETURN)
        assert (g.state, g.level_index, g.score, g.kills) == ('playing', 0, 0, 0)
        assert g.path == first_path
        key(pygame.K_p)
        click(g.ui.secondary_rect)
        assert g.state == 'menu'
        print('PASS: Chinese menu, card clicks, pause/guide isolation, map refunds, results and restart')
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
