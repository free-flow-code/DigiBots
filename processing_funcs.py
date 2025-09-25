import random
from typing import Iterator, List, Dict, Tuple, Union

from bots import HerbivoreBot, PlantBot
from settings import settings
from bot_factory import BotFactory

BotType = Union[HerbivoreBot, PlantBot]


def create_bots() -> List[BotType]:
    """Создаёт список ботов с уникальными начальными позициями (без пересечений).

    Тип бота (подвижный/неподвижный) выбирается случайно в соответствии с
    параметром settings.STATIC_FRACTION (доля неподвижных). Если этот параметр
    отсутствует — используется 0.5 (половина/половина).

    Чтобы избежать бесконечного ожидания на плотных полях, для каждой попытки
    генерации позиции есть ограничение max_attempts — после его исчерпания бот
    создаётся в любой случайной позиции (даже если есть пересечение).

    Returns:
        list[Bot]: Список инициализированных ботов.
    """
    bots: List[BotType] = []
    static_fraction: float = getattr(settings, "STATIC_FRACTION", 0.5)
    max_attempts = getattr(settings, "CREATE_MAX_ATTEMPTS", 2000)

    for _ in range(settings.NUM_BOTS):
        attempts = 0
        while True:
            attempts += 1
            x = random.randint(settings.BOT_RADIUS, settings.SCREEN_W - settings.BOT_RADIUS)
            y = random.randint(settings.BOT_RADIUS, settings.SCREEN_H - settings.BOT_RADIUS)

            # Проверяем пересечения с уже созданными ботами
            good = True
            for b in bots:
                dx = x - b.x
                dy = y - b.y
                rsum = settings.BOT_RADIUS + b.r
                if dx * dx + dy * dy < rsum * rsum:
                    good = False
                    break

            if good:
                bots.append(BotFactory.create_random(x, y, static_fraction))
                break

            # Фолбэк: если слишком много неудачных попыток — создаём бота без проверки
            if attempts >= max_attempts:
                bots.append(BotFactory.create_random(x, y, static_fraction))
                break

    return bots


def build_grid(bots: List[BotType]) -> Dict[Tuple[int, int], List[int]]:
    """Создаёт пространственную сетку (spatial hash) для ускорения поиска коллизий.

    Args:
        bots (list[Bot]): Список ботов.

    Returns:
        dict[tuple[int, int], list[int]]: Словарь, где ключ — координаты ячейки сетки,
        а значение — список индексов ботов, находящихся в этой ячейке.
    """
    grid: Dict[Tuple[int, int], List[int]] = {}
    for i, b in enumerate(bots):
        if not b.alive:  # мёртвые не участвуют
            continue
        b.update_cell()
        key = (b.cell_x, b.cell_y)
        grid.setdefault(key, []).append(i)
    return grid


def neighbor_cells(cx: int, cy: int) -> Iterator[Tuple[int, int]]:
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
    grid: Dict[Tuple[int, int], List[int]],
    bots: List[BotType],
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
            if dx * dx + dy * dy < rsum * rsum:
                return True
    return False
