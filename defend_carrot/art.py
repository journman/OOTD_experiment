"""Cached procedural fruit art, shared by towers, cards and placement previews."""
from functools import lru_cache

import pygame

import config as C


@lru_cache(maxsize=24)
def fruit_image(kind, size=40, flash=False):
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
