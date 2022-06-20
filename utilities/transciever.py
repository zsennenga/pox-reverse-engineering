from rflib import SYNCM_16_of_16, RfCat, MOD_ASK_OOK

from const.bit_timings import freq, baud
from const.sync_bits import SIGNATURE_TX
from model.pox_advertise import PoxAdvertise


def get_transciever() -> RfCat:
    d = RfCat()
    d.setFreq(freq)
    d.setMdmSyncWord(0b1010101010101100)
    d.setMdmModulation(MOD_ASK_OOK)
    d.setMdmDRate(baud)
    d.setModeIDLE()

    return d


def rx_packet(d: RfCat) -> bytes:
    d.setMdmSyncMode(SYNCM_16_of_16)
    d.setModeRX()
    d.makePktFLEN(40)
    pkt, _ = d.RFrecv(timeout=30000)
    d.setModeIDLE()
    return pkt


def rx_pox(d: RfCat) -> PoxAdvertise:
    pkt = rx_packet(d)
    return PoxAdvertise.from_encoded_bytes(pkt)


def tx_packet(d: RfCat, packet: bytes) -> None:
    d.setMdmSyncMode(0)
    d.setMaxPower()
    target_bytes = SIGNATURE_TX + packet
    d.makePktFLEN(len(target_bytes))
    d.setModeTX()
    d.RFxmit(target_bytes)
    d.setModeIDLE()
