from abc import ABC, abstractmethod

from settings import settings


class MovementStrategy(ABC):
    @abstractmethod
    def move(self, x: float, y: float) -> tuple[float, float]:
        pass


class LinearMovement(MovementStrategy):
    """Возвращает новые координаты с учётом wrap-around
    (боты выходят с одной стороны экрана и появляются с другой).
    """

    def __init__(self, vx: int, vy: int):
        self.vx = vx
        self.vy = vy

    def move(self, x: float, y: float) -> tuple[float, float]:
        new_x, new_y = x + self.vx, y + self.vy

        # wrap-around
        if new_x < 0:
            new_x = settings.SCREEN_W
        elif new_x > settings.SCREEN_W:
            new_x = 0
        if new_y < 0:
            new_y = settings.SCREEN_H
        elif new_y > settings.SCREEN_H:
            new_y = 0

        return new_x, new_y


class StationaryMovement(MovementStrategy):
    """Не двигается."""

    def move(self, x: float, y: float) -> tuple[float, float]:
        return x, y
