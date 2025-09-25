import pygame
import random
from settings import settings
from processing_funcs import build_grid, collides_with_any, create_bots
from resources import SCREEN, CLOCK, GRASS_SURF

pygame.init()

# Создаём ботов через фабрику
bots = create_bots()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Убираем мёртвых ботов
    bots = [b for b in bots if b.alive]

    # Перестраиваем spatial hash grid
    grid = build_grid(bots)

    # Рисуем фон
    SCREEN.blit(GRASS_SURF, (0, 0))

    # Двигаем и рисуем всех ботов
    for index, bot in enumerate(bots):
        old_x, old_y = bot.x, bot.y

        bot.update_position()
        new_x, new_y = bot.x, bot.y

        if collides_with_any(new_x, new_y, bot.r, index, grid, bots):
            bot.on_collision()

            # После смены стратегии движения пробуем снова
            bot.update_position()
            new_x, new_y = bot.x, bot.y

            # Если всё ещё коллизия — откат + небольшое случайное смещение, чтобы не застрять
            bot.x, bot.y = old_x + random.choice([-1, 1]), old_y + random.choice([-1, 1])

        bot.update_cell()
        pygame.draw.circle(SCREEN, bot.color, (int(bot.x), int(bot.y)), bot.r)

    pygame.display.flip()
    CLOCK.tick(settings.FPS)

pygame.quit()
