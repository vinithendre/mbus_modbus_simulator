from checkSum import CheckSum
import numpy as np
import logger
import constants as const
import converter as conv


_logger = logger.create_logger('CheckSuLRC')

class CheckSumLRC(CheckSum):
    Name = 'LRC'
    def __init__(self):
        pass
    def calculate_byte (self, value, history):
        return (history + value) & 0xFF


    def calculate (self, frame):
        sum = 0
        for byte in frame:
            if isinstance(byte, str):
                byte = ord(byte)
            sum = self.calculate_byte(byte, sum)
        return sum


    def calculate_and_append_lcr (self, frame_as_hexstring):
        frame_for_calc = []
        frame_for_calc = frame_as_hexstring[12:]

        arr = conv.convert_frame_string_to_int_array(frame_for_calc)

        csum = str(hex(self.calculate(arr)))[2:]
        csum = csum.zfill(2).upper()

        frame_len = str(hex(len(frame_for_calc.split())))[2:]

        frame_prefix = f"68 {frame_len} {frame_len} 68 "
        frame_postfix = f" {csum} 16"

        _logger.info(f"Calculated checksum from the frame is {csum}")
        frame_for_calc = frame_prefix + frame_for_calc + frame_postfix
        return frame_for_calc
