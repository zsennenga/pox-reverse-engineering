from enum import Enum


class Wad(Enum):
    H = "H"
    B = "B"
    T = "T"
    #OUT_OF_RANGE = "OOR"

WAD_MAP: dict[int, Wad] = {
    0: Wad.H,  # Head
    1: Wad.B,  # Body
    2: Wad.T,  # Tail
    #3: Wad.OUT_OF_RANGE,
}

INVERTED_WAD_MAP: dict[Wad, int] = {v: k for k, v in WAD_MAP.items()}
