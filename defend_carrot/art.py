"""Cached procedural fruit art, shared by towers, cards and placement previews."""
from functools import lru_cache
from pathlib import Path

import pygame

import config as C

ASSET_DIR = Path(__file__).resolve().parent / 'assets'
# Pixel regions of the original 1774x887 sheet. Wings and leaves extend beyond
# nominal grid boundaries, so explicit regions keep entire silhouettes intact.
CHARACTERS = {
    'apple': (43, 49, 379, 391), 'orange': (467, 65, 411, 376),
    'melon': (913, 68, 463, 376), 'carrot': (1400, 12, 331, 434),
    'slime': (26, 489, 390, 356), 'bat': (422, 501, 506, 300),
    'golem': (929, 472, 474, 382), 'thrower': (1425, 460, 309, 386),
}


@lru_cache(maxsize=4)
def load_image(name):
    path = ASSET_DIR / name
    if not path.is_file():
        return None
    return pygame.image.load(str(path))


@lru_cache(maxsize=96)
def character_image(kind, size=40, flash=False):
    atlas = load_image('character-atlas.png')
    if atlas is None:
        return None
    cell = atlas.subsurface(pygame.Rect(CHARACTERS[kind]))
    bounds = cell.get_bounding_rect(min_alpha=12)
    if not bounds.w or not bounds.h:
        return None
    sprite = cell.subsurface(bounds)
    scale = (size - 2) / max(bounds.size)
    dimensions = (max(1, round(bounds.w * scale)), max(1, round(bounds.h * scale)))
    image = pygame.Surface((size, size), pygame.SRCALPHA)
    sprite = pygame.transform.smoothscale(sprite, dimensions)
    if flash:
        sprite.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_ADD)
    image.blit(sprite, sprite.get_rect(center=(size // 2, size // 2)))
    return image


def fruit_image(kind, size=40, flash=False):
    image = character_image(kind, size, flash)
    return image if image is not None else _fallback_fruit_image(kind, size, flash)


@lru_cache(maxsize=24)
def _fallback_fruit_image(kind, size=40, flash=False):
    image = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.ellipse(image, (20, 40, 24, 70), (6, 36, 36, 9))
    color = (255, 247, 222) if flash else C.FRUITS[kind]['color']
    edge = (44, 78, 37)
    if kind == 'apple':
        pygame.draw.ellipse(image, edge, (6, 12, 36, 30))
        pygame.draw.ellipse(image, color, (8, 13, 32, 26))
        pygame.draw.line(image, (91, 62, 33), (24, 15), (26, 6), 3)
        pygame.draw.ellipse(image, (116, 181, 70), (26, 5, 12, 7))
    elif kind == 'orange':
        pygame.draw.circle(image, edge, (24, 25), 18)
        pygame.draw.circle(image, color, (24, 25), 16)
        pygame.draw.ellipse(image, (86, 154, 59), (23, 5, 13, 8))
        for pos in ((13, 29), (34, 21), (31, 35)):
            pygame.draw.circle(image, (212, 116, 28), pos, 1)
    else:
        pygame.draw.ellipse(image, edge, (4, 10, 40, 32))
        pygame.draw.ellipse(image, color, (6, 12, 36, 28))
        for x in (14, 23, 32):
            pygame.draw.arc(image, (42, 117, 63), (x - 6, 12, 13, 28), -1.1, 1.1, 3)
    pygame.draw.ellipse(image, (255, 255, 225, 130), (11, 16, 9, 5))
    for x in (18, 29):
        pygame.draw.circle(image, (255, 253, 220), (x, 26), 4)
        pygame.draw.circle(image, (32, 45, 32), (x + 1, 26), 2)
    pygame.draw.arc(image, edge, (20, 29, 10, 7), 3.3, 6.0, 2)
    return pygame.transform.smoothscale(image, (size, size))
