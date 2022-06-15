import random

from ai.base import BaseAi
from const.wad import Wad
from model.pox_advertise import PoxAdvertise

wads = {Wad.H, Wad.B, Wad.T}

class LoserAI(BaseAi):
    def pcu_id(self, incoming_pox: PoxAdvertise):
        return "LOSER "

    def pox_name(self, incoming_pox: PoxAdvertise):
        return "LOSER "

    def random_wad_except(self, not_wad: Wad) -> Wad:
        return random.choice(list(wads - {not_wad}))

    def wad(self, incoming_pox: PoxAdvertise):
        return [
            self.rand_wad(),
            incoming_pox.wad[2],
            self.random_wad_except(incoming_pox.wad[1]),
            self.rand_wad(),
            incoming_pox.wad[5],
            self.random_wad_except(incoming_pox.wad[4]),
            self.rand_wad(),
            incoming_pox.wad[8],
            self.random_wad_except(incoming_pox.wad[7]),
        ]
