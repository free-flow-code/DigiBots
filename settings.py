from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Window
    SCREEN_W: int = 640
    SCREEN_H: int = 480
    FPS: int = 60

    # Bots
    NUM_BOTS: int = 1000
    BOT_RADIUS: int = 5
    BOT_COLOR: tuple[int, int, int] = (0, 0, 0)

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
