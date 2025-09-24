import random
from typing import Iterator

from bots import Bot
from settings import settings


def create_bots() -> list[Bot]:
    """Создаёт список ботов с уникальными начальными позициями (без пересечений).

    Боты размещаются случайным образом внутри экрана так,
    чтобы их радиусы не пересекались друг с другом.

    Returns:
        list[Bot]: Список инициализированных ботов.
    """
    bots = []
    for _ in range(settings.NUM_BOTS):
        while True:
            x = random.randint(settings.BOT_RADIUS, settings.SCREEN_W - settings.BOT_RADIUS)
            y = random.randint(settings.BOT_RADIUS, settings.SCREEN_H - settings.BOT_RADIUS)

            # Проверка на пересечение с уже созданными ботами
            good = True
            for b in bots:
                dx = x - b.x
                dy = y - b.y
                if dx*dx + dy*dy < (settings.BOT_RADIUS*2) ** 2:
                    good = False
                    break
            if good:
                vx = random.choice([-1, 1])
                vy = random.choice([-1, 1])
                bots.append(Bot(x, y, vx, vy))
                break

    return bots


# Build grid
def build_grid(bots: list[Bot]) -> dict[tuple[int, int], list[int]]:
    """Создаёт пространственную сетку (spatial hash) для ускорения поиска коллизий.

    Args:
        bots (list[Bot]): Список ботов.

    Returns:
        dict[tuple[int, int], list[int]]: Словарь, где ключ — координаты ячейки сетки,
        а значение — список индексов ботов, находящихся в этой ячейке.
    """
    grid = {}
    for i, b in enumerate(bots):
        b.update_cell()
        key = (b.cell_x, b.cell_y)
        grid.setdefault(key, []).append(i)
    return grid


def neighbor_cells(cx: int, cy: int) -> Iterator[tuple[int, int]]:
    """Генерирует координаты соседних ячеек вокруг заданной.

    Перебирает все 9 ячеек вокруг бота:
        текущую (0,0)
        по горизонтали (-1,0, 1,0)
        по вертикали (0,-1, 0,1)
        и диагонали (-1,-1, 1,-1, -1,1, 1,1).
    Где OFFS - кортеж смещений по осям:
        -1 означает «соседняя ячейка слева / сверху»
        0 означает «текущая ячейка»
        1 означает «соседняя ячейка справа / снизу»

    То есть бот ищет потенциальные коллизии только среди объектов в
    своей ячейке и соседних, а не во всём списке ботов.

    Args:
        cx (int): Координата ячейки по X.
        cy (int): Координата ячейки по Y.

    Yields:
        tuple[int, int]: Координаты соседней ячейки (nx, ny).
    """
    for dx in settings.OFFS:
        nx = cx + dx
        if nx < 0 or nx >= settings.GRID_W:
            continue
        for dy in settings.OFFS:
            ny = cy + dy
            if ny < 0 or ny >= settings.GRID_H:
                continue
            yield (nx, ny)


def collides_with_any(
    x: float,
    y: float,
    r: int,
    bot_index: int,
    grid: dict[tuple[int, int], list[int]],
    bots: list[Bot],
) -> bool:
    """Проверяет, сталкивается ли бот с другими ботами поблизости.

    Args:
        x (float): Новая координата X бота.
        y (float): Новая координата Y бота.
        r (int): Радиус бота.
        bot_index (int): Индекс текущего бота (чтобы не сравнивать с самим собой).
        grid (dict[tuple[int, int], list[int]]): Пространственная сетка с индексами ботов.
        bots (list[Bot]): Список всех ботов.

    Returns:
        bool: True, если есть столкновение, иначе False.
    """
    cx = int(x) // settings.CELL_SIZE
    cy = int(y) // settings.CELL_SIZE
    for cell in neighbor_cells(cx, cy):
        if cell not in grid:
            continue
        for j in grid[cell]:
            if j == bot_index:
                continue
            other = bots[j]
            dx = x - other.x
            dy = y - other.y
            rsum = r + other.r
            if dx*dx + dy*dy < rsum*rsum:
                return True
    return False
