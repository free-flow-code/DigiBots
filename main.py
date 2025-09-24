import pygame

from settings import settings
from processing_funcs import create_bots, \
    build_grid, \
    collides_with_any
from resources import SCREEN, CLOCK, GRASS_SURF

pygame.init()

bots = create_bots()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Перестраиваем spatial hash grid для ускоренной проверки коллизий
    grid = build_grid(bots)
    # Отрисовка заднего фона (трава уже прорисована заранее)
    SCREEN.blit(GRASS_SURF, (0, 0))

    # Двигаем и рисуем всех ботов
    for i, b in enumerate(bots):
        nx, ny = b.move_with_wrap()

        # Проверка коллизий
        if collides_with_any(nx, ny, b.r, i, grid, bots):
            # меняем направление на случайное при столкновении
            b.bounce_randomly()
            nx, ny = b.move_with_wrap()
            # второй шанс: если всё ещё коллизия, просто оставляем текущее положение
            if collides_with_any(nx, ny, b.r, i, grid, bots):
                nx, ny = b.x, b.y

        b.x, b.y = nx, ny
        b.update_cell()
        pygame.draw.circle(SCREEN, b.color, (int(b.x), int(b.y)), b.r)

    pygame.display.flip()
    CLOCK.tick(settings.FPS)

pygame.quit()
