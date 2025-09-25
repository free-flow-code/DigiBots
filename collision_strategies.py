import random
from abc import ABC, abstractmethod

from movement_strategies import LinearMovement


class CollisionStrategy(ABC):
    @abstractmethod
    def on_collision(self, bot: "BotBase") -> None:
        pass


class RandomDirectionChange(CollisionStrategy):
    """Случайно меняет направление движения после столкновения."""

    def on_collision(self, bot: "BotBase") -> None:
        if random.random() < 0.5:
            bot.movement = LinearMovement(
                random.choice([-1, 0, 1]),
                random.choice([-1, 0, 1])
            )


class DieOnCollision(CollisionStrategy):
    """После столкновения бот умирает."""

    def on_collision(self, bot: "BotBase") -> None:
        bot.alive = False
