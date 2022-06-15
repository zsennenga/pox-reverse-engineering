import random
from dataclasses import dataclass

from const.chars import CHAR_MAP
from const.parts import head_values, body_values, tail_values
from const.pox_color import PcuColor
from const.wad import Wad
from model.pox_advertise import PoxAdvertise


@dataclass
class Parameters:
    head_id: int = None
    head_hp: int = None
    body_id: int = None
    body_hp: int = None
    tail_id: int = None
    tail_hp: int = None
    pcu_color: PcuColor = None
    pcu_id: str = None
    pox_name: str = None
    wad: list[Wad] = None
    died_from_reinfector: bool = False


class BaseAi:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters

    def random_string(self):
        return "".join(random.choice(list(CHAR_MAP.values())) for _ in range(6))

    def pcu_id(self, incoming_pox: PoxAdvertise):
        raise NotImplementedError

    def pox_name(self, incoming_pox: PoxAdvertise):
        raise NotImplementedError

    def rand_hp(self, min_=30, max_=500):
        return random.randint(min_, max_)

    def rand_wad(self):
        return random.choice(list(Wad))

    def wad(self, incoming_pox: PoxAdvertise):
        return [self.rand_wad() for _ in range(10)]

    def pcu_color(self, incoming_pox: PoxAdvertise):
        return random.choice(list(PcuColor))

    def head_id(self, incoming_pox: PoxAdvertise):
        return random.choice(head_values)

    def body_id(self, incoming_pox: PoxAdvertise):
        return random.choice(body_values)

    def tail_id(self, incoming_pox: PoxAdvertise):
        return random.choice(tail_values)

    def head_hp(self, incoming_pox: PoxAdvertise):
        return self.rand_hp()

    def body_hp(self, incoming_pox: PoxAdvertise):
        return self.rand_hp()

    def tail_hp(self, incoming_pox: PoxAdvertise):
        return self.rand_hp()

    def build_pox(self, incoming_pox: PoxAdvertise) -> PoxAdvertise:
        return PoxAdvertise(
            head_id=self.parameters.head_id or self.head_id(incoming_pox),
            head_hp=self.parameters.head_hp or self.head_hp(incoming_pox),
            body_id=self.parameters.body_id or self.body_id(incoming_pox),
            body_hp=self.parameters.body_hp or self.body_hp(incoming_pox),
            tail_id=self.parameters.tail_id or self.tail_id(incoming_pox),
            tail_hp=self.parameters.tail_hp or self.tail_hp(incoming_pox),
            wad=self.parameters.wad or self.wad(incoming_pox),
            pcu_id=self.parameters.pcu_id or self.pcu_id(incoming_pox),
            pox_name=self.parameters.pox_name or self.pox_name(incoming_pox),
            pcu_color=self.parameters.pcu_color or self.pcu_color(incoming_pox),
            died_from_reinfector=self.parameters.died_from_reinfector,
        )
