from enum import Enum


class PcuColor(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    #DEV = "dev"


COLOR_MAP = {
    PcuColor.RED: 0,
    PcuColor.GREEN: 1,
    PcuColor.BLUE: 2,
    #PcuColor.DEV: 3,
}

INVERTED_COLOR_MAP: dict[int, PcuColor] = {v: k for k, v in COLOR_MAP.items()}
