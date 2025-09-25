import random
from typing import List, Type
from settings import settings
from bots import PlantBot, HerbivoreBot

BotType = PlantBot | HerbivoreBot  # можно расширять, если появятся новые


class BotFactory:
    _registry: dict[str, Type[BotType]] = {}

    @classmethod
    def register(cls, kind: str, bot_cls: Type[BotType]) -> None:
        """Регистрирует новый тип бота."""
        cls._registry[kind] = bot_cls

    @classmethod
    def create(cls, kind: str, x: int, y: int) -> BotType:
        """Создаёт одного бота по типу."""
        if kind not in cls._registry:
            raise ValueError(f"Unknown bot type: {kind}")
        return cls._registry[kind](x, y)

    @classmethod
    def create_many(cls, kind: str, quantity: int, bots: List[BotType]) -> List[BotType]:
        """Создаёт несколько ботов определённого типа без пересечений."""
        result: List[BotType] = []

        for _ in range(quantity):
            x, y = cls._find_free_position(bots + result)
            result.append(cls.create(kind, x, y))

        return result

    @staticmethod
    def _find_free_position(existing: List[BotType]) -> tuple[int, int]:
        """Подбирает позицию без пересечений (или возвращает случайную после max_attempts).

        Чтобы избежать бесконечного ожидания на плотных полях, для каждой попытки
        генерации позиции есть ограничение max_attempts — после его исчерпания бот
        создаётся в любой случайной позиции (даже если есть пересечение).
        """
        for _ in range(settings.CREATE_MAX_ATTEMPTS):
            x = random.randint(settings.BOT_RADIUS, settings.SCREEN_W - settings.BOT_RADIUS)
            y = random.randint(settings.BOT_RADIUS, settings.SCREEN_H - settings.BOT_RADIUS)

            # Проверяем пересечения с уже созданными ботами
            good = True
            for b in existing:
                dx = x - b.x
                dy = y - b.y
                rsum = settings.BOT_RADIUS + b.r
                if dx * dx + dy * dy < rsum * rsum:
                    good = False
                    break

            if good:
                return x, y

        # fallback
        return (
            random.randint(settings.BOT_RADIUS, settings.SCREEN_W - settings.BOT_RADIUS),
            random.randint(settings.BOT_RADIUS, settings.SCREEN_H - settings.BOT_RADIUS),
        )
