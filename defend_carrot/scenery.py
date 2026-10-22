"""Original backgrounds and road textures adapted to the gameplay waypoints."""
from functools import lru_cache
import math

import pygame

import config as C
from art import load_image, atlas_frame


def _round_path(surface, color, points, width):
    pygame.draw.lines(surface, color, False, points, width)
    for point in points:
        pygame.draw.circle(surface, color, point, width // 2)


@lru_cache(maxsize=2)
def field_image(index):
    level = C.LEVELS[index]
    image = pygame.Surface((C.FIELD_W, C.FIELD_H))
    theme = index + 1
    terrain = atlas_frame(f'Themes/Theme{theme}/BG0/BG1-hd', 'BG1.png')
    if terrain is not None:
        image.blit(pygame.transform.smoothscale(terrain, image.get_size()), (0, 0))
    else:
        image.fill(level['grass'][0])
    points = [(col * C.TILE + C.TILE // 2, row * C.TILE + C.TILE // 2)
              for col, row in level['path']]
    road = load_image(f'original/Themes/Theme{theme}/BG1/BG-hd.png')
    if road is not None and index == 0:
        # Only scenery is copied from the old map; its baked route is never
        # displayed beneath our different, interactive route.
        decorations = ((0, 330, 310, 152), (705, 330, 255, 152))
        for i, area in enumerate(decorations):
            piece = road.subsurface(area)
            piece = pygame.transform.smoothscale(piece, (180, 90))
            image.blit(piece, (0 if i == 0 else C.FIELD_W - 180, C.FIELD_H - 90))
    edge, fill = ((80, 181, 220), (216, 247, 255)) if index == 0 else (
        (128, 177, 20), (192, 144, 0))
    _round_path(image, edge, points, C.TILE + 8)
    _round_path(image, fill, points, C.TILE - 2)
    if road is not None:
        # Sample an original straight road tile, including its painted edges.
        area = (180, 240, 80, 80) if index == 0 else (100, 0, 100, 100)
        tile = pygame.transform.smoothscale(road.subsurface(area), (C.TILE, C.TILE + 8))
        for start, end in zip(points, points[1:]):
            distance = math.dist(start, end)
            ux, uy = ((end[0] - start[0]) / distance, (end[1] - start[1]) / distance)
            piece = tile if ux else pygame.transform.rotate(tile, 90)
            for step in range(C.TILE // 2, round(distance), C.TILE):
                center = (round(start[0] + ux * step), round(start[1] + uy * step))
                image.blit(piece, piece.get_rect(center=center))
    # The endpoint and entrance cues occupy their real path cells.
    x, y = points[-1]
    pygame.draw.ellipse(image, edge, (x - 23, y - 15, 46, 32))
    pygame.draw.ellipse(image, fill, (x - 21, y - 15, 42, 27))
    x, y = points[0]
    dx, dy = points[1][0] - x, points[1][1] - y
    x, y = max(13, min(C.FIELD_W - 14, x)), max(13, min(C.FIELD_H - 14, y))
    arrow = ([(x - 5, y - 7), (x + 5, y), (x - 5, y + 7)] if dx else
             [(x - 7, y - 5), (x, y + 5), (x + 7, y - 5)])
    pygame.draw.polygon(image, (116, 98, 61), arrow)
    return image
