import pygame

from settings import settings


def make_grass_surf(step: int = 2) -> pygame.Surface:
    """Создаёт поверхность с "травой" (зелёные точки на фоне).

    Args:
        step (int, optional): Расстояние между точками. По умолчанию 2.

    Returns:
        pygame.Surface: Поверхность с прорисованной травой.
    """
    surf = pygame.Surface((settings.SCREEN_W, settings.SCREEN_H))
    surf.fill(settings.BG_COLOR)
    for x in range(0, settings.SCREEN_W, step):
        for y in range(0, settings.SCREEN_H, step):
            surf.fill(settings.GRASS_COLOR, (x, y, 1, 1))
    return surf


# Инициализация только ресурсов pygame
SCREEN = pygame.display.set_mode((settings.SCREEN_W, settings.SCREEN_H))
pygame.display.set_caption("DigiBots")
CLOCK = pygame.time.Clock()
GRASS_SURF = make_grass_surf()
