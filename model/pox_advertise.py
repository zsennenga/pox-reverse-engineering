import crc16
from bitstring import Bits

from const.chars import CHAR_MAP, INVERTED_CHAR_MAP
from const.manchester import MANCHESTER_MAP, INVERSE_MANCHESTER_MAP
from const.pox_color import PcuColor, INVERTED_COLOR_MAP, COLOR_MAP
from const.wad import Wad, INVERTED_WAD_MAP, WAD_MAP
from model.schema import PoxAdvertiseStruct
from utilities.flipper import get_bitstrings_from_sub_file


def validate_unknown(unknown: int):
    if unknown > 3 or unknown < 0:
        raise ValueError("unknown must be between 0 and 3")


class PoxAdvertise:
    def __init__(
            self,
            head_id: int,
            head_hp: int,
            body_id: int,
            body_hp: int,
            tail_id: int,
            tail_hp: int,
            wad: list[Wad],
            pcu_id: str,
            pox_name: str,
            pcu_color: PcuColor,
            died_from_reinfector: bool = False
    ):
        if len(pcu_id) != 6:
            raise ValueError("PCU ID must be 6 characters long")
        if len(pox_name) != 6:
            raise ValueError("POX Name must be 6 characters long")
        if len(wad) != 9:
            raise ValueError("WAD must be 9 elements long")

        if head_hp > 511 or head_hp < 30:
            raise ValueError("Head HP must be between 30 and 511")
        if body_hp > 511 or body_hp < 30:
            raise ValueError("Body HP must be between 30 and 511")
        if tail_hp > 511 or tail_hp < 30:
            raise ValueError("Tail HP must be between 30 and 511")


        self.head_id = head_id
        self.head_hp = head_hp
        self.body_id = body_id
        self.body_hp = body_hp
        self.tail_id = tail_id
        self.tail_hp = tail_hp
        self.wad = wad
        self.pcu_id = pcu_id
        self.pox_name = pox_name
        self.pcu_color = pcu_color
        self.died_from_reinfector = died_from_reinfector

    @classmethod
    def extract_wad(cls, packed: int) -> Wad:
        return WAD_MAP[cls.extract_small_int(packed)]

    @classmethod
    def extract_char(cls, packed: int) -> str:
        return CHAR_MAP[packed & 0b00111111]

    @classmethod
    def extract_bool(cls, packed: int) -> bool:
        return packed & 0b01000000 != 0

    @classmethod
    def extract_int(cls, packed: int) -> int:
        return packed & 0b00111111

    @classmethod
    def extract_small_int(cls, packed: int) -> int:
        return packed >> 6

    @classmethod
    def pack_wad_char(cls, wad: Wad, char_: str) -> int:
        return (INVERTED_WAD_MAP[wad] << 6) | INVERTED_CHAR_MAP[char_]

    @classmethod
    def pack_bool_char(cls, bool_: bool, char_: str) -> int:
        return (int(bool_) << 6) | INVERTED_CHAR_MAP[char_]

    @classmethod
    def pack_int_char(cls, int_: int, char_: str) -> int:
        return (int_ << 6) | INVERTED_CHAR_MAP[char_]

    @classmethod
    def pack_dual_bool_char(cls, bool_1: bool, bool_2: bool, char_: str) -> int:
        return (int(bool_1) << 7) | (int(bool_2) << 6) | INVERTED_CHAR_MAP[char_]

    @classmethod
    def calculate_crc(cls, bytes_: bytes) -> bytes:
        return crc16.crc16xmodem(bytes_).to_bytes(2, byteorder='big')

    @classmethod
    def decode_bytes(cls, bitstring: str) -> bytes:
        """
        Decode a bitstring into a bytes object.
        :param bitstring: a string of 1s and 0s representing a manchester encoded rf signal
        :return: the underlying bytes
        """
        decoded = "0b"
        for i in range(0, len(bitstring), 2):
            decoded += MANCHESTER_MAP[bitstring[i:i + 2]]

        return Bits(decoded).bytes

    @classmethod
    def from_sub_file(cls, filename: str) -> list["PoxAdvertise"]:
        bitstrings = get_bitstrings_from_sub_file(filename=filename)
        return [cls.from_encoded_bitstring(bitstring) for bitstring in bitstrings]

    @classmethod
    def from_encoded_bitstring(cls, bitstring: str) -> "PoxAdvertise":
        bytes_ = cls.decode_bytes(bitstring)
        return cls.from_bytes(bytes_)

    @classmethod
    def from_encoded_bytes(cls, bytes_: bytes) -> "PoxAdvertise":
        bitstring = ""
        for bit in Bits(bytes_):
            if bit:
                bitstring += '1'
            else:
                bitstring += '0'
        return cls.from_encoded_bitstring(bitstring)

    @classmethod
    def from_bytes(cls, bytes_: bytes) -> "PoxAdvertise":
        crc = cls.calculate_crc(bytes_[:-2])
        if crc != bytes_[-2:]:
            raise ValueError("CRC does not match")
        struct = PoxAdvertiseStruct.parse(bytes_)

        head_hp = struct.head_hp
        body_hp = struct.body_hp
        tail_hp = struct.tail_hp
        # Uppermost bit
        if struct.head_hp256_bit_body_hp256_bit_pox_name4 & 0b10000000 != 0:
            head_hp = head_hp + 256
        # Next bit
        if struct.head_hp256_bit_body_hp256_bit_pox_name4 & 0b01000000 != 0:
            body_hp = body_hp + 256
        # Uppermost bit
        if struct.tail_hp256_bit_died_reinfector_bit_pox_name5 & 0b10000000 != 0:
            tail_hp = tail_hp + 256

        died_from_reinfector = struct.tail_hp256_bit_died_reinfector_bit_pox_name5 & 0b01000000 != 0

        return cls(
            head_id=struct.head_id,
            head_hp=head_hp,
            body_id=struct.body_id,
            body_hp=body_hp,
            tail_id=struct.tail_id,
            tail_hp=tail_hp,
            wad=[
                cls.extract_wad(struct.wad0_id0),
                cls.extract_wad(struct.wad1_id1),
                cls.extract_wad(struct.wad2_id2),
                cls.extract_wad(struct.wad3_id3),
                cls.extract_wad(struct.wad4_id4),
                cls.extract_wad(struct.wad5_id5),
                cls.extract_wad(struct.wad6_pox_name0),
                cls.extract_wad(struct.wad7_pox_name1),
                cls.extract_wad(struct.wad8_pox_name2),
            ],
            pcu_id=(
                    cls.extract_char(struct.wad0_id0) +
                    cls.extract_char(struct.wad1_id1) +
                    cls.extract_char(struct.wad2_id2) +
                    cls.extract_char(struct.wad3_id3) +
                    cls.extract_char(struct.wad4_id4) +
                    cls.extract_char(struct.wad5_id5)
            ),
            pox_name=(
                    cls.extract_char(struct.wad6_pox_name0) +
                    cls.extract_char(struct.wad7_pox_name1) +
                    cls.extract_char(struct.wad8_pox_name2) +
                    cls.extract_char(struct.pcu_color_pox_name3) +
                    cls.extract_char(struct.head_hp256_bit_body_hp256_bit_pox_name4) +
                    cls.extract_char(struct.tail_hp256_bit_died_reinfector_bit_pox_name5)
            ),
            pcu_color=INVERTED_COLOR_MAP[cls.extract_small_int(struct.pcu_color_pox_name3)],
            died_from_reinfector=died_from_reinfector,
        )

    def _inner_struct_bytes(self, crc: bytes = b"\x00\x00") -> bytes:
        return PoxAdvertiseStruct.build(
            dict(
                head_id=self.head_id,
                head_hp=self.head_hp % 256,
                body_id=self.body_id,
                body_hp=self.body_hp % 256,
                tail_id=self.tail_id,
                tail_hp=self.tail_hp % 256,
                wad0_id0=self.pack_wad_char(self.wad[0], self.pcu_id[0]),
                wad1_id1=self.pack_wad_char(self.wad[1], self.pcu_id[1]),
                wad2_id2=self.pack_wad_char(self.wad[2], self.pcu_id[2]),
                wad3_id3=self.pack_wad_char(self.wad[3], self.pcu_id[3]),
                wad4_id4=self.pack_wad_char(self.wad[4], self.pcu_id[4]),
                wad5_id5=self.pack_wad_char(self.wad[5], self.pcu_id[5]),
                wad6_pox_name0=self.pack_wad_char(self.wad[6], self.pox_name[0]),
                wad7_pox_name1=self.pack_wad_char(self.wad[7], self.pox_name[1]),
                wad8_pox_name2=self.pack_wad_char(self.wad[8], self.pox_name[2]),
                pcu_color_pox_name3=self.pack_int_char(COLOR_MAP[self.pcu_color], self.pox_name[3]),
                head_hp256_bit_body_hp256_bit_pox_name4=self.pack_dual_bool_char(
                    self.head_hp >= 256,
                    self.body_hp >= 256,
                    self.pox_name[4]
                ),
                tail_hp256_bit_died_reinfector_bit_pox_name5=self.pack_dual_bool_char(
                    self.tail_hp >= 256,
                    self.died_from_reinfector,
                    self.pox_name[5]
                ),
                crc=crc
            )
        )

    def to_bytes(self) -> bytes:
        return self._inner_struct_bytes(self.calculate_crc(self._inner_struct_bytes()[:-2]))

    def to_encoded_bytes(self) -> bytes:
        bitstring = ""
        for bit in Bits(self.to_bytes()):
            if bit:
                bitstring += '1'
            else:
                bitstring += '0'
        encoded_bitstring = "0b"
        for bit in bitstring:
            encoded_bitstring += INVERSE_MANCHESTER_MAP[bit]

        return Bits(encoded_bitstring).tobytes()
