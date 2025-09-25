from settings import settings
from movement_strategies import MovementStrategy, LinearMovement, StationaryMovement
from collision_strategies import CollisionStrategy, DieOnCollision, RandomDirectionChange


class BotBase:
    """Абстрактный базовый класс для ботов.

    Бот имеет позицию (x, y), радиус, цвет,
    принадлежность к ячейке пространственной сетки, состояние (жив/мертв),
    стратегии движения и столкновений.
    """

    __slots__ = ("x", "y", "r", "color", "cell_x", "cell_y",
                 "alive", "movement", "collision")

    def __init__(
        self,
        x: float,
        y: float,
        r: int,
        color: tuple[int, int, int],
        movement: MovementStrategy,
        collision: CollisionStrategy,
    ) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.cell_x = 0
        self.cell_y = 0
        self.alive = True

        # зависимости внедряются через стратегии
        self.movement = movement
        self.collision = collision

    def set_color(self, color: tuple[int, int, int]) -> None:
        self.color = color

    def update_cell(self) -> None:
        """Обновляет координаты ячейки сетки.

        Используется для пространственного хэширования, чтобы ускорить
        поиск столкновений с соседними объектами.
        """
        self.cell_x = int(self.x) // settings.CELL_SIZE
        self.cell_y = int(self.y) // settings.CELL_SIZE

    def update_position(self) -> None:
        """Обновляет координаты согласно стратегии движения."""
        self.x, self.y = self.movement.move(self.x, self.y)

    def on_collision(self) -> None:
        """Реакция на столкновение по стратегии."""
        self.collision.on_collision(self)


# ====== Specific bots ======

class HerbivoreBot(BotBase):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(
            x=x,
            y=y,
            r=settings.BOT_RADIUS,
            color=settings.HERBIVORE_BOT_COLOR,
            movement=LinearMovement(
                settings.HERBIVORE_BOT_SPEED["vx"],
                settings.HERBIVORE_BOT_SPEED["vy"],
            ),
            collision=RandomDirectionChange(),
        )


class PlantBot(BotBase):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(
            x=x,
            y=y,
            r=settings.BOT_RADIUS,
            color=settings.PLANT_BOT_COLOR,
            movement=StationaryMovement(),
            collision=DieOnCollision(),
        )
