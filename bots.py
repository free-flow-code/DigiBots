import random

from settings import settings


class Bot:
    """Класс, описывающий "бота" (частицу) в симуляции.

    Бот имеет позицию (x, y), скорость (vx, vy), радиус, цвет
    и принадлежность к ячейке пространственной сетки.
    """
    __slots__ = ("x", "y", "vx", "vy", "r", "color", "cell_x", "cell_y")

    def __init__(self,
                 x: float,
                 y: float,
                 vx: float,
                 vy: float,
                 r: int = settings.BOT_RADIUS,
                 color: tuple[int, int, int] = settings.BOT_COLOR
                 ) -> None:
        """Создаёт объект бота.

        Args:
            x (float): Начальная координата X.
            y (float): Начальная координата Y.
            vx (float): Скорость по оси X.
            vy (float): Скорость по оси Y.
            r (int, optional): Радиус бота. По умолчанию settings.BOT_RADIUS.
            color (tuple[int, int, int], optional): Цвет бота (RGB).
               По умолчанию settings.BOT_COLOR.
        """
        self.x: float = x
        self.y: float = y
        self.vx: float = vx
        self.vy: float = vy
        self.r: int = r
        self.color: tuple[int, int, int] = color
        self.cell_x: int = 0
        self.cell_y: int = 0

    def update_cell(self) -> None:
        """Обновляет координаты ячейки сетки, в которой находится бот.

        Используется для пространственного хэширования, чтобы ускорить
        поиск столкновений с соседними объектами.
        """
        self.cell_x = int(self.x) // settings.CELL_SIZE
        self.cell_y = int(self.y) // settings.CELL_SIZE

    def move_with_wrap(self) -> tuple[float, float]:
        """Возвращает новые координаты с учётом wrap-around
        (боты выходят с одной стороны и появляются с другой).
        """
        nx, ny = self.x + self.vx, self.y + self.vy
        if nx < 0:
            nx = settings.SCREEN_W
        elif nx > settings.SCREEN_W:
            nx = 0
        if ny < 0:
            ny = settings.SCREEN_H
        elif ny > settings.SCREEN_H:
            ny = 0
        return nx, ny

    def bounce_randomly(self) -> None:
        """Меняет направление движения на случайное."""
        self.vx = random.choice([-1, 1])
        self.vy = random.choice([-1, 1])
