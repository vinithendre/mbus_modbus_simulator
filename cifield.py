from dataclasses import dataclass
from converter import convert_hexstring_to_int
import logger
import constants as const


@dataclass
class CIField:

    def __init__(self, value):
        self.subcode_describtion = None
        self._logger = logger.create_logger(' ci-field ')
        self.len_of_frame = None
        self.ci_field_string = value
        self.ci_field = convert_hexstring_to_int(value)
        self.application_msg = const.CiFieldType.NONE
        self.type_of_error = None
        self.purpose_sent_telegram = None
        self.error_detail = None
        self.error= False
        self.set_len_field(value)
        self.set_purpose_of_the_sent_telegram(value)
        self.print_global_variable()
        self.set_subcode(value)


    def set_len_field(self, value):
        self.len_of_frame = value


    def print_global_variable(self):
        value = f"The ci-Field charakter =  '{self.ci_field_string}' present following: <br/> \
                  self.len_of_frame = {self.len_of_frame}<br/> \
                  application_msg = {self.application_msg}<br/> \
                  self.purpose_sent_telegram = {self.purpose_sent_telegram}<br/> \
                  self.subcode_describtion  = {self.subcode_describtion}<br/>"
        self._logger.info(value)


    def set_purpose_of_the_sent_telegram(self, value):
        value_int = convert_hexstring_to_int(value)
        if value_int == 0x51:
            self.application_msg = const.CiFieldType.MASTER_DATA_SEND
            self.purpose_sent_telegram = "data send"
        elif value_int == 0x52:
            self.application_msg = const.CiFieldType.SLAVE_SELECTION
            self.purpose_sent_telegram = "selection of slaves"
        elif value_int == 0x55:
            self.application_msg = const.CiFieldType.MASTER_DATA_SEND
            self.purpose_sent_telegram = "data send (LSB first)"
        elif value_int == 0x56:
            self.application_msg = const.CiFieldType.SLAVE_SELECTION
            self.purpose_sent_telegram = "selection of slaves (LSB first)"
        elif value_int == 0x50:
            self.application_msg = const.CiFieldType.RESET_APLLICATION_LEVEL
            self.purpose_sent_telegram = "application reset"
        elif value_int == 0x54:
            self.application_msg = const.CiFieldType.SLAVE_SYNC_FROM_MASTER
            self.purpose_sent_telegram = "synronize action"
        elif value_int == 0xB8:
            self.application_msg = const.CiFieldType.MASTER_BAUDRATE_SET_COMMAND
            self.purpose_sent_telegram = "set baudrate to 300 baud"
        elif value_int == 0xB9:
            self.application_msg = const.CiFieldType.MASTER_BAUDRATE_SET_COMMAND
            self.purpose_sent_telegram = "set baudrate to 600 baud"
        elif value_int == 0xBA:
            self.application_msg = const.CiFieldType.MASTER_BAUDRATE_SET_COMMAND
            self.purpose_sent_telegram = "set baudrate to 1200 baud"
        elif value_int == 0xBB:
            self.application_msg = const.CiFieldType.MASTER_BAUDRATE_SET_COMMAND
            self.purpose_sent_telegram = "set baudrate to 2400 baud"
        elif value_int == 0xBC:
            self.application_msg = const.CiFieldType.MASTER_BAUDRATE_SET_COMMAND
            self.purpose_sent_telegram = "set baudrate to 4800 baud"
        elif value_int == 0xBD:
            self.application_msg = const.CiFieldType.MASTER_BAUDRATE_SET_COMMAND
            self.purpose_sent_telegram = "set baudrate to 9600 baud "
        elif value_int == 0xBE:
            self.application_msg = const.CiFieldType.MASTER_BAUDRATE_SET_COMMAND
            self.purpose_sent_telegram = "set baudrate to 19200 baud"
        elif value_int == 0xBF:
            self.application_msg = const.CiFieldType.MASTER_BAUDRATE_SET_COMMAND
            self.purpose_sent_telegram = "set baudrate to 38400 baud"
        elif value_int == 0xB1:
            self.application_msg = const.CiFieldType.MASTER_ASK_FOR_RAM_PRINTING
            self.purpose_sent_telegram = "request readout of complete ram content"
        elif value_int == 0xB2:
            self.application_msg = const.CiFieldType.MASTER_WRITE_RAM
            self.purpose_sent_telegram = "send user data (not standardized ram write) "
        elif value_int == 0xB3:
            self.application_msg = const.CiFieldType.MASTER_START_CALIBRATION_TEST
            self.purpose_sent_telegram = "initialize test calibration mode "
        elif value_int == 0xB4:
            self.application_msg = const.CiFieldType.MASTER_READ_EPROM    
            self.purpose_sent_telegram = "eprom read"
        elif value_int == 0xB6:
            self.application_msg = const.CiFieldType.MASTER_STARTS_SOFTWARE_TEST
            self.purpose_sent_telegram = "start software test"
        elif value_int in range (0x90 ,0x97):
            self.application_msg = const.CiFieldType.CODE_FOR_HASH_VERIFY
            self.purpose_sent_telegram = "codes used for hashing obsolete and should no longer be needed"
            self._logger.warning(f"code --> {value_int},  '{self.purpose_sent_telegram}'")
        elif value_int == 0x70:
            self.error= True
            self.application_msg = const.CiFieldType.REPORT_GENERAL_APPLICATION_ERROR
            self.purpose_sent_telegram = "report of general application errors "
            self.set_error_detail(value_int)
        elif value_int == 0x71:
            self.application_msg = const.CiFieldType.REPORT_ALARM_STATUS
            self.purpose_sent_telegram = "report of alarm status "
        elif value_int == 0x72:
            self.application_msg = const.CiFieldType.VARIABLE_DATA_RESPOND
            self.purpose_sent_telegram = "variable data respond en1434-3 "
        elif value_int == 0x73:
            self.application_msg = const.CiFieldType.FIXED_DATA_RESPOND
            self.purpose_sent_telegram = "fixed data respond en1434-3 "
        elif value_int == 0x76:
            self.application_msg = const.CiFieldType.VARIABLE_DATA_RESPOND
            self.purpose_sent_telegram = "variable data respond en1434-3 (LSB first)"
        elif value_int == 0x77:
            self.application_msg = const.CiFieldType.FIXED_DATA_RESPOND
            self.purpose_sent_telegram = "fixed data respond en1434-3 (LSB first)"
        else:
            err_msg = f"Unknown ci-Field code -->(value_int --> {value_int})"
            self._logger.error(err_msg)
            raise Exception (err_msg)


    def set_error_detail(self, value):
        value_int = convert_hexstring_to_int(value)
        if value_int == 0x70:
            self.error_detail = "report of general application errors "
        elif value_int == 0x71:
            self.error_detail = "report of alarm status "
        elif value_int == 0x72:
            self.error_detail = "variable data respond en1434-3 "
        elif value_int == 0x73:
            self.error_detail = "fixed data respond en1434-3 "
        elif value_int == 0x76:
            self.error_detail = "variable data respond en1434-3 "
        elif value_int == 0x77:
            self.error_detail = "fixed data respond en1434-3 "
        else:
            err_msg = f"Unknown ci-Field error detail -->(value_int --> {value_int})"
            self._logger.error(err_msg)
            raise Exception (err_msg)


    def set_general_application_errors(self, value):
        value_int = convert_hexstring_to_int(value)
        if value_int ==  0:
            self.type_of_error = "unspecified error: also if data field is missing"
        elif value_int ==  1:
            self.type_of_error = "unimplemented ci-field"
        elif value_int ==  2:
            self.type_of_error = "buffer too long, truncated"
        elif value_int ==  3:
            self.type_of_error = "too many records"
        elif value_int ==  4:
            self.type_of_error = "premature end of record"
        elif value_int ==  5:
            self.type_of_error = "more than 10 dife's"
        elif value_int ==  6:
            self.type_of_error = "more than 10 vife's"
        elif value_int ==  7:
            self.type_of_error = "reserved "
        elif value_int ==  8:
            self.type_of_error = "application too busy for handling readout request"
        elif value_int ==  9:
            self.type_of_error = "too many readouts (for slaves with limited readouts per time)"
        elif value_int in range(10,256):
            self.type_of_error = "reserved"
        else:
            err_msg = f"Unknown ci-Field general application error -->(value --> {value})"
            self._logger.error(err_msg)
            raise Exception (err_msg)


    def set_subcode(self, value):
        value_int = convert_hexstring_to_int(value)
        mask_data_length = 0b00001111
        value_mask = value_int & mask_data_length

        if value_mask == 0:
            self.subcode_describtion ="all"
        elif value_mask == 1:
            self.subcode_describtion ="user data (consumption)"
        elif value_mask == 2:
            self.subcode_describtion ="simple billing (actual and fixed date values+dates)"
        elif value_mask == 3:
            self.subcode_describtion ="enhanced billing (historic values)"
        elif value_mask == 4:
            self.subcode_describtion ="multi tariff billing"
        elif value_mask == 5:
            self.subcode_describtion ="instaneous values (for regulation)"
        elif value_mask == 6:
            self.subcode_describtion ="load management values for management"
        elif value_mask == 7:
            self.subcode_describtion ="reserved"
        elif value_mask == 8:
            self.subcode_describtion ="installation and startup (bus adress, fixed dates)"
        elif value_mask == 9:
            self.subcode_describtion ="testing (high resolution values)"
        elif value_mask == 10:
            self.subcode_describtion ="calibration"
        elif value_mask == 11:
            self.subcode_describtion ="manufacturing"
        elif value_mask == 12:
            self.subcode_describtion ="development"
        elif value_mask == 13:
            self.subcode_describtion ="selftest"
        elif value_mask == 14:
            self.subcode_describtion ="reserved"
        elif value_mask == 15:
            self.subcode_describtion ="reserved"
        else:
            self.subcode_describtion ="No subcode found in Application reseet subcode"
