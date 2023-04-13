import enum


# Generell definition
CONFIG_SIMMULATORMODE_MODBUS = "modbus"
CONFIG_SIMMULATORMODE_MBUS = "mbus"

# Modbus definition
ENDIANNES_BIG = 'big'
ENDIANNES_LITTLE = 'little'

DATATYPE_FLOAT64 = 'float64'
DATATYPE_UINT16 = 'uint16'
DATATYPE_UINT32 = 'uint32'
DATATYPE_UINT64 = 'uint64'

ALLOWED_FUNCTION_CODE_MODBUS = [1, 2, 3, 4, 6]
FUNCTION_CODE_WITH_READONLY = [1, 2, 3, 4]


# Field indexes
START_CHAR_IDX = 0
STOP_CHAR_IDX = -1 # -1 = last element in list
CHECK_SUM_IDX = -2

# Mbus specified data
START_CHAR_SHORT = 0x10
START_CHAR_LONG = 0x68
STOP_CHAR = 0x16
ACK_CHAR = 0xE5


#throw following away
CI_FIELD_IDX = 6

C_FIELD_IDX_SHORT = 1
C_FIELD_IDX_LONG = 4
A_FIELD_IDX_SHORT = 2
A_FIELD_IDX_LONG = 5

FRAME_LEN_SINGLE = 1
FRAME_LEN_SHORT = 5
FRAME_LEN_CTRL = 9 # longer frame than this => long frame

USER_DATA_START = 7
USER_DATA_END = -2  # = last element is len - 3 when used for list indexing


# Function Field
FUNC_FIELD_NAME_INSTANTANEOUS_VALUE = "Instantaneous value"
FUNC_FIELD_NAME_MAXIMUM_VALUE = "Maximum value"
FUNC_FIELD_NAME_MINIMUM_VALUE = "Minimum value"
FUNC_FIELD_NAME_DURING_ERROR = "Value during error stat"

FUNC_FIELD_KEY_INSTANTANEOUS_VALUE = 0
FUNC_FIELD_KEY_MAXIMUM_VALUE = 1
FUNC_FIELD_KEY_MINIMUM_VALUE = 2
FUNC_FIELD_KEY_VALUE_DURING_ERROR = 3





# M-bus definition
DEFAULT_VALUE_PRIMARY_ADDR = 253
PRIMARY_ADDR_MIN_VALUE = 0
PRIMARY_ADDR_MAX_VALUE = 250


# M-bus definition & Modbus definition
class FrameType(enum.Enum):
    FRAMETYPE_ERROR = -1
    NONE = 0
    LONG = 1
    CONTROL = 2
    SHORT = 3
    SINGLE = 4


class CommunicationDirection(enum.Enum):
    NONE = 0
    CALLING = 1
    REPLY = 2


class CiFieldType(enum.Enum):
    NONE = 0
    REPORT_GENERAL_APPLICATION_ERROR = 1
    REPORT_ALARM_STATUS = 2
    VARIABLE_DATA_RESPOND = 3
    FIXED_DATA_RESPOND = 4
    MASTER_DATA_SEND = 6
    SLAVE_SELECTION = 7
    RESET_APLLICATION_LEVEL = 8
    SLAVE_SYNC_FROM_MASTER = 9
    MASTER_BAUDRATE_SET_COMMAND = 10
    MASTER_ASK_FOR_RAM_PRINTING = 11
    MASTER_WRITE_RAM = 12
    MASTER_START_CALIBRATION_TEST = 13
    MASTER_READ_EPROM = 14
    MASTER_STARTS_SOFTWARE_TEST = 15
    CODE_FOR_HASH_VERIFY = 16


class CodingDataField(enum.Enum):
    NONE = 0
    DATA_FIELD = 1
    VARIABLE_LENGTH = 2
    SPECIAL_FUNCTIONS = 3


class VifType(enum.Enum):
    NONE = 0
    PRIMARY_VIF = 1
    PLAIN_TEXT_INFORMATION = 2
    LINEAR_VIF_EXTENSION = 3
    VIF_IN_FOLLOWING_STRING = 4
    ANY_VIF = 5
    MANUFACTOR_SPECIFICATION = 6
    STANDARD = 1


class Lvar(enum.Enum):
    NONE = 0
    ASCI_STRING_WITH_LVAR_CHARS = 1
    POSITIVE_BCD_NUMBER = 2
    NEGATIVE_BCD_NUMBER = 3
    BINARY_NUMBER = 4
    FLOATING_POINT_NUMBER = 5
    RESERVED = 6


class SpecialFunction (enum.Enum):
    NONE = 0
    MANUFACTOR_SPECIFIC_DATA_STRUCTURE = 1
    MORE_RECORDS_FOLLOW_IN_NEXT_TELEGRAM = 2
    IDLE_FILLER = 3
    RESERVED = 4
    GLOBAL_READOUT_REQUEST = 5


class DataLengthMeaning (enum.Enum):
    NONE = 0
    NO_DATA = 1
    INTEGER = 2
    REAL = 3
    SELECTION_FOR_READOUT = 4
    BCD = 5
    VARIABLE_LENGTH = 6
    SPECIAL_FUNCTION = 7
