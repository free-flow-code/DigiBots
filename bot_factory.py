import random

from bots import HerbivoreBot, PlantBot


class BotFactory:
    """Фабрика для создания ботов разных типов."""

    @staticmethod
    def create_herbivore(x: int, y: int) -> HerbivoreBot:
        return HerbivoreBot(x, y)

    @staticmethod
    def create_plant(x: int, y: int) -> PlantBot:
        return PlantBot(x, y)

    @staticmethod
    def create_random(x: int, y: int, static_fraction: float = 0.5):
        """Создаёт случайного бота в указанной позиции."""
        if random.random() < static_fraction:
            return BotFactory.create_plant(x, y)
        return BotFactory.create_herbivore(x, y)
