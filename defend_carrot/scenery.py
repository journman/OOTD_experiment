"""Cached painted terrain with roads drawn from the exact gameplay waypoints."""
from functools import lru_cache
import math
import random

import pygame

import config as C
from art import load_image


def _round_path(surface, color, points, width):
    pygame.draw.lines(surface, color, False, points, width)
    for point in points:
        pygame.draw.circle(surface, color, point, width // 2)


@lru_cache(maxsize=2)
def field_image(index):
    level = C.LEVELS[index]
    image = pygame.Surface((C.FIELD_W, C.FIELD_H))
    terrain = load_image('garden-ground.png' if index == 0 else 'forest-ground.png')
    if terrain is not None:
        image.blit(pygame.transform.smoothscale(terrain, image.get_size()), (0, 0))
    else:
        image.fill(level['grass'][0])
    points = [(col * C.TILE + C.TILE // 2, row * C.TILE + C.TILE // 2)
              for col, row in level['path']]
    shadow = [(x, y + 3) for x, y in points]
    _round_path(image, (87, 91, 53), shadow, C.TILE + 7)
    _round_path(image, (156, 126, 78), points, C.TILE + 3)
    _round_path(image, (222, 196, 147), points, C.TILE - 2)
    _round_path(image, (233, 211, 168), points, C.TILE - 11)
    rng = random.Random(2026 + index)
    for start, end in zip(points, points[1:]):
        distance = math.dist(start, end)
        ux, uy = ((end[0] - start[0]) / distance, (end[1] - start[1]) / distance)
        for step in range(12, round(distance), 20):
            side = rng.choice((-1, 1)) * rng.randint(11, 15)
            x = round(start[0] + ux * step - uy * side)
            y = round(start[1] + uy * step + ux * side)
            pygame.draw.ellipse(image, (186, 161, 115), (x, y, 5, 3))
            pygame.draw.line(image, (242, 224, 184), (x, y), (x + 3, y))
    # The endpoint and entrance cues occupy their real path cells.
    x, y = points[-1]
    pygame.draw.ellipse(image, (145, 110, 56), (x - 23, y - 15, 46, 32))
    pygame.draw.ellipse(image, (232, 196, 105), (x - 21, y - 15, 42, 27))
    pygame.draw.ellipse(image, (250, 225, 154), (x - 17, y - 12, 34, 20), 2)
    x, y = points[0]
    dx, dy = points[1][0] - x, points[1][1] - y
    x, y = max(13, min(C.FIELD_W - 14, x)), max(13, min(C.FIELD_H - 14, y))
    arrow = ([(x - 5, y - 7), (x + 5, y), (x - 5, y + 7)] if dx else
             [(x - 7, y - 5), (x, y + 5), (x + 7, y - 5)])
    pygame.draw.polygon(image, (116, 98, 61), arrow)
    return image
