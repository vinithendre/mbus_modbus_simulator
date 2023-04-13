from dataclasses import dataclass
import logger
import constants as const
from converter import convert_hexstring_to_int


@dataclass
class CField:

    def __init__(self, value, frame_type):
        self.c_field_string = value
        self.c_field = convert_hexstring_to_int(value)
        self._logger = logger.create_logger('  c-field ')
        self.bit8 = None
        self.bit7 = None
        self.fcb = None
        self.fcv = None
        self.acd = None
        self.dfc = None
        self.f_3 = None
        self.f_2 = None
        self.f_1 = None
        self.f_0 = None
        self.communication_dir = None
        self.frame_type = frame_type
        self.get_parsed_details(value)
        self.set_coding_of_control_field(value)


    def get_parsed_details(self, value):
        self.get_parsed_details_control_and_long_frame(value)

    def get_parsed_details_control_and_long_frame(self, value):
        value_int = convert_hexstring_to_int(value)
        self.communication_dir = const.CommunicationDirection.NONE
        if value_int == 0x40:
            self.communication_dir = const.CommunicationDirection.CALLING
            self._logger.info(
                "Comand 'SND_NKE' short frame (Initialization of Slave)")
        elif value_int in [0x53, 0x73]:
            self._logger.info(
                "Comand 'SND_UD' long/control frame (Send User Data to Slave)")
            self.communication_dir = const.CommunicationDirection.CALLING
        elif value_int in [0x5B, 0x7B]:
            self._logger.info(
                "Comand 'REQ_UD2' short frame (Request for Class 2 Data)")
            self.communication_dir = const.CommunicationDirection.CALLING
            if value_int == 0x5b:
                self._logger.info(
                    "Comand 'REQ_UD2' with a FCB (cField-code = {value})")
            elif value_int == 0x7b:
                self._logger.info(
                    "Comand 'REQ_UD2' WITHOUT FCB  (cField-code = {value})")
        elif value_int in [0x5A, 0x7A]:
            self._logger.info(
                "Comand 'REQ_UD1' short frame (Request for Class1 Data)")
            self.communication_dir = const.CommunicationDirection.CALLING
        elif value_int in [0x08, 0x18, 0x28, 0x38]:
            self.communication_dir = const.CommunicationDirection.REPLY
            self._logger.info("Comand 'RSP_UD' long/control frame (Data Transfer from Slave to Master after Request)")
        else:
            self._logger.error("The cField (cField-code = {value}) does not correspond to the \
                                expected value according to the MBus specification. The values \
                                ​​{arr_req_ud2}' and '{arr_req_ud1}' are only allowed")

    def set_coding_of_control_field(self, value):
        self.fcb = None
        self.fcv = None
        self.acd = None
        self.dfc = None

        value_int = convert_hexstring_to_int(value)
        if self.communication_dir == const.CommunicationDirection.CALLING:
            mask_fcb = 0b00100000
            self.fcb = value_int & mask_fcb > 0

            mask_fcv = 0b00010000
            self.fcv = value_int & mask_fcv > 0
        elif self.communication_dir == const.CommunicationDirection.REPLY:
            mask_acd = 0b00100000
            self.acd = value_int & mask_acd > 0

            mask_dfc = 0b00010000
            self.dfc = value_int & mask_dfc > 0
        else:
            err_msg = "Communication direction is not defined!"
            self._logger.error(err_msg)
            raise Exception(err_msg)

        mask_bit8 = 0b10000000
        self.bit8 = value_int & mask_bit8 > 0

        mask_bit7 = 0b00000001
        self.bit7 = value_int & mask_bit7 > 0

        mask_f0 = 0b00000001
        self.f_0 = value_int & mask_f0 > 0

        mask_f1 = 0b00000010
        self.f_1 = value_int & mask_f1 > 0

        mask_f2 = 0b00000100
        self.f_2 = value_int & mask_f2 > 0

        mask_f3 = 0b00001000
        self.f_3 = value_int & mask_f3 > 0

    def print_global_variable(self):
        value = f"The c-Field charakter =  '{self.c_field_string}' present following: <br/> \
                  bit8  =  {self.bit8} <br/> \
                  bit7  =  {self.bit7} <br/> \
                  f3  =  {self.f_3} <br/> \
                  f2  =  {self.f_2} <br/> \
                  f1  =  {self.f_1} <br/> \
                  f0  =  {self.f_0} <br/>"
        if self.communication_dir == const.CommunicationDirection.CALLING:
            value = value + f"fcb  =  {self.fcb} <br/> \
                              fcv  =  {self.fcv} <br/>"
        elif self.communication_dir == const.CommunicationDirection.REPLY:
            value = value + f"acd  =  {self.acd} <br/> \
                              dfc  =  {self.dfc} <br/> \
                              frame_type = {self.frame_type} <br/> \
                              communication_dir = {self.communication_dir} <br/>"
        else:
            err_msg = f"With communication dir {self.communication_dir} there is no support"
            self._logger.error(err_msg)
            raise Exception(err_msg)
        self._logger.info(value)
