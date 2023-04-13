from dataclasses import dataclass
import logger
from converter import convert_hexstring_to_int


@dataclass
class AField:
    address = None

    def __init__(self, value):
        self._logger = logger.create_logger('  a-field ')
        self.primary_address = None
        self.a_field_string = value
        self.a_field = convert_hexstring_to_int(value)
        self.meaning = None
        self.get_parsed_details(value)


    def get_parsed_details(self, value):
        value_int = convert_hexstring_to_int(value)
        self.primary_address = value_int

        allowed_value = range(0, 255)
        allowed_prim_addresses = range(1, 250)
        if value_int in allowed_value:
            self.address = value_int
            if value_int == 0:
                self.meaning = f"Unconfigured slaves with the default address '{value}' at manufacture. This means that the MBus slave is reset to the manufacturer's address or a primary address has never been set!"
            elif value_int in allowed_prim_addresses:
                self.meaning = f"Configured slaves with the address between {allowed_prim_addresses}. Current primary address is '{value_int}'"
                # TODO Hans --> Update the device with this serial number
            elif value_int == 253:
                self.meaning = f"the adressing has been performed in the Network Layer (address = '{value}')"
            elif value_int in [254, 255]:
                self.meaning = f"Transmit information to all participants (Broadcast) (address = '{value}')"
            else:
                self.meaning = f"This value is not allowed and is therefore not processed. This value '{value}' should not be sent by the master."
        else:
            self.meaning = f"The aField does not correspond to the expected value according to the MBus specification. The values '​​{allowed_value}' are only allowed"
        

    def print_global_variable(self):
        value = f"The a-Field charakter =  '{self.a_field_string}' present following: <br/> \
                  Primary_address = {self.primary_address}<br/> \
                  Meaning = {self.meaning}<br/>"
        self._logger.info(value)
