import sys
import time

from rflib import ChipconUsbTimeoutException

from ai.base import Parameters, BaseAi
from ai.bully import BullyAI
from ai.loser import LoserAI
from ai.random import RandomAI
from model.pox_advertise import PoxAdvertise
from utilities.transciever import get_transciever, rx_packet, tx_packet

AI: dict[str, type[BaseAi]] = {
    'bully': BullyAI,
    'random': RandomAI,
    'loser': LoserAI,

}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <ai_name>")
        sys.exit(1)
    parameters = Parameters()
    ai: BaseAi = AI[sys.argv[1]](parameters)
    transciever = get_transciever()
    while True:
        try:
            try:
                print("Waiting for packet...")
                pkt = rx_packet(transciever)
                pox = PoxAdvertise.from_encoded_bytes(pkt)
                print(f"Got pox on RX {pox.pcu_id}:{pox.pox_name}")
            except ChipconUsbTimeoutException:
                print("Timed out on rx... trying again")
                continue
            except Exception as e:
                print("Got error!")
                print(e.__class__.__name__, e)
                continue
            ai_pox = ai.build_pox(pox)
            if pox.pcu_id == ai_pox.pcu_id:
                print('We already beat them! Sleep until I see someone new...')
                continue
            print(f"Sending pox {ai_pox.pcu_id}:{ai_pox.pox_name}")
            for _ in range(3):
                print("Sending...")
                tx_packet(transciever, ai_pox.to_encoded_bytes())
                time.sleep(5)
        except KeyboardInterrupt:
            print("Exiting...")
            transciever.setModeIDLE()
            sys.exit(0)


