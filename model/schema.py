from construct import Struct, Int8ul, Bytes

PoxAdvertiseStruct = Struct(
    "head_id" / Int8ul,
    "head_hp" / Int8ul,
    "body_id" / Int8ul,
    "body_hp" / Int8ul,
    "tail_id" / Int8ul,
    "tail_hp" / Int8ul,
    "wad0_id0" / Int8ul * "upper two bits are upper left wad, lower 6 bits are id char 0",
    "wad1_id1" / Int8ul * "upper two bits are upper middle wad, lower 6 bits are id char 1",
    "wad2_id2" / Int8ul * "upper two bits are upper right wad, lower 6 bits are id char 2",
    "wad3_id3" / Int8ul * "upper two bits are middle left wad, lower 6 bits are id char 3",
    "wad4_id4" / Int8ul * "upper two bits are middle middle wad, lower 6 bits are id char 4",
    "wad5_id5" / Int8ul * "upper two bits are middle right wad, lower 6 bits are id char 5",
    "wad6_pox_name0" / Int8ul * "upper two bits are lower left wad, lower 6 bits are pox name char 0",
    "wad7_pox_name1" / Int8ul * "upper two bits are lower middle wad, lower 6 bits are pox name char 1",
    "wad8_pox_name2" / Int8ul * "upper two bits are lower right wad, lower 6 bits are pox name char 2",
    "pcu_color_pox_name3" / Int8ul * "upper two bits are life status, lower 6 bits are pox name char 3",
    "head_hp256_bit_body_hp256_bit_pox_name4" / Int8ul * "upper two bits mark the head and body as having 256 hp, lower 6 bits are pox name char 4",
    "tail_hp256_bit_died_reinfector_bit_pox_name5" / Int8ul * "uppermost bit declares the tail has 256 hp, next bit declares that pox was defeated by a second-order invader (IE pcu 1 -> pcu 2 -> me), lower 6 bits are pox name char 5",
    "crc" / Bytes(2) * "crc-16 xmodem"
)
