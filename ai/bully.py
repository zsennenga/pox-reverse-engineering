from ai.base import BaseAi
from const.wad import Wad
from model.pox_advertise import PoxAdvertise


class BullyAI(BaseAi):
    def pcu_id(self, incoming_pox: PoxAdvertise):
        return "BULLY "

    def pox_name(self, incoming_pox: PoxAdvertise):
        return "BULLY "

    def head_hp(self, incoming_pox: PoxAdvertise):
        return 500

    def body_hp(self, incoming_pox: PoxAdvertise):
        return 500

    def tail_hp(self, incoming_pox: PoxAdvertise):
        return 500

    def weakest_wad(
            self,
            defending: Wad,
            sorted_wads: list[Wad]
    ):
        for wad in sorted_wads:
            if wad != defending:
                return wad

    def wad(self, incoming_pox: PoxAdvertise):
        parts_by_hp = [
            _[0] for _ in sorted(
            [
                (Wad.H, incoming_pox.head_hp),
                (Wad.B, incoming_pox.body_hp),
                (Wad.T, incoming_pox.tail_hp),
            ],
            key=lambda x: x[1]
        )
        ]
        return [
            self.rand_wad(),
            self.weakest_wad(
                incoming_pox.wad[2],
                parts_by_hp
            ),
            incoming_pox.wad[1],
            self.rand_wad(),
            self.weakest_wad(
                incoming_pox.wad[5],
                parts_by_hp
            ),
            incoming_pox.wad[4],
            self.rand_wad(),
            self.weakest_wad(
                incoming_pox.wad[8],
                parts_by_hp
            ),
            incoming_pox.wad[7],
        ]
