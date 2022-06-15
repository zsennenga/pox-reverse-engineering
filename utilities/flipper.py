import re

from const.bit_timings import on_bitlen, off_bitlin
from const.sync_bits import SIGNATURE_RX_BITSTRING


def get_timings_from_file(filename: str) -> list[int]:
    segs = []
    with open(filename, 'r') as f:
        for line in f:
            m = re.match(r'RAW_Data:\s*([-0-9 ]+)\s*$', line)
            if m:
                segs.extend([int(seg) for seg in m[1].split(r' ')])
    return segs

def get_raw_bitstring_from_sub_file(filename: str) -> str:
    segs = get_timings_from_file(filename)
    decoded_bits = []
    for seg in segs:
        if seg > 0:
            ones = round(seg / on_bitlen)
            decoded_bits.extend('1' * ones)
        elif seg < 0:
            zeros = round(-seg / off_bitlin)
            decoded_bits.extend('0' * zeros)
    return ''.join(decoded_bits)


def get_bitstrings_from_sub_file(filename: str) -> list[str]:
    full_bitstring = get_raw_bitstring_from_sub_file(filename)

    bitstrings = []
    for group in re.finditer(SIGNATURE_RX_BITSTRING, full_bitstring):
        pos = group.end()
        data = full_bitstring[pos:pos + 320]
        bitstrings.append(data)

    return bitstrings
