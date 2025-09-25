from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Window
    SCREEN_W: int = 640
    SCREEN_H: int = 480
    FPS: int = 60

    # Bots
    NUM_BOTS: int = 100
    BOT_RADIUS: int = 5

    DEFAULT_BOT_COLOR: tuple[int, int, int] = (0, 0, 0)
    PLANT_BOT_COLOR: tuple[int, int, int] = (34, 136, 34)
    HERBIVORE_BOT_COLOR: tuple[int, int, int] = (34, 34, 136)

    DEFAULT_BOT_SPEED: dict[str, int] = {'vx': 5, 'vy': 5}
    PLANT_BOT_SPEED: dict[str, int] = {'vx': 0, 'vy': 0}
    HERBIVORE_BOT_SPEED: dict[str, int] = {'vx': 5, 'vy': 5}

    # Colors
    BG_COLOR: tuple[int, int, int] = (255, 255, 255)
    GRASS_COLOR: tuple[int, int, int] = (0, 150, 0)

    # Spatial hash grid
    CELL_SIZE: int = 32
    OFFS: tuple[int, int, int] = (-1, 0, 1)

    @property
    def GRID_W(self) -> int:
        return (self.SCREEN_W + self.CELL_SIZE - 1) // self.CELL_SIZE

    @property
    def GRID_H(self) -> int:
        return (self.SCREEN_H + self.CELL_SIZE - 1) // self.CELL_SIZE


settings = Settings()
