from ai.base import BaseAi
from model.pox_advertise import PoxAdvertise


class RandomAI(BaseAi):
    def pcu_id(self, incoming_pox: PoxAdvertise):
        return "RANDY "

    def pox_name(self, incoming_pox: PoxAdvertise):
        return self.random_string()