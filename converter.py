from datetime import datetime
import struct
import binascii
import logger
import math
_logger = logger.create_logger('Converter ')


def float_to_hex(value_float):
    value = hex(struct.unpack('<Q', struct.pack('<d', value_float))[0])
    if str(value).lower() == '0x0':
        return '0x0000000000000000'
    return value


def hex_to_float(value_hex):
    value_float, = struct.unpack('>d', binascii.unhexlify(value_hex.encode()))
    return value_float


def get_2digit_hex_array_from_hexstring(hex_string):
    if (hex_string[0:2]).upper() == '0X':
        split_string = []
        step = 2
        for i in range(2, len(hex_string), step):
            split_string.append(format_hexstring_to_2digit_wellformated_hex_string(hex_string[i:i + step]))
        return split_string
    else:
        raise Exception(f"The input string value '{hex_string}' is not a hex string")


def get_2digit_string_array_from_string(value, array_reversed=False):
    split_string = []
    step = 2
    for i in range(0, len(value), step):
        split_string.append(value[i:i + step].zfill(2))
    if array_reversed:
        split_string.reverse()
    return split_string


def convert_hexstring_to_hex(hex_as_string):
    if (hex_as_string[0:2]).upper() == '0X':
        value_int = int(hex_as_string, 16)
        hex_value = hex(value_int)
        return hex_value
    else:
        raise Exception(f"The input string value '{hex_as_string}' is not a hex string")


def convert_hexstring_to_int(hex_as_string):
    if isinstance(hex_as_string, int):
        value_int = hex_as_string
    else:
        value_int = int(hex_as_string, 16)
    return value_int


def convert_string_hexarray_to_frame(arr):
    frame_val = [int(x, base=16) for x in arr]
    return bytes(frame_val)


def decimal_to_hex(n):
    hex_string = __decimal_to_hex(n)
    return hex_string


def __decimal_to_hex(value_decimal):
    conv_val = (value_decimal % 16)
    char_placholder = ""
    if conv_val < 10:
        char_placholder = conv_val
    if conv_val == 10:
        char_placholder = "A"
    if conv_val == 11:
        char_placholder = "B"
    if conv_val == 12:
        char_placholder = "C"
    if conv_val == 13:
        char_placholder = "D"
    if conv_val == 14:
        char_placholder = "E"
    if conv_val == 15:
        char_placholder = "F"
    if value_decimal - conv_val != 0:
        return __decimal_to_hex(value_decimal // 16) + str(char_placholder)
    else:
        return str(char_placholder)


def get_nippel_array_from_hex(value):
    arr = []
    arrhex = convert_hexstring_to_hex(value)
    array_length = len(arrhex)
    for i in range(2, array_length):
        arr.append(arrhex[i])
    return arr


def get_bits_from_hexval(value_hex):
    res = F"{convert_hexstring_to_int(value_hex):08b}"
    return res


def get_bits_from_int(int_val, length):
    res = f"{int_val:b}".zfill(length)
    return res


def __get_nippel_from_hex(val, n):
    #example of this function:  Input:'0xE62' --> Output: ['e', '6', '2']
    arr = get_nippel_array_from_hex(val)
    return int(f'0x{arr[n]}', 16)


def get_first_nippel_from_hex(val):
    arr = get_nippel_array_from_hex(val)
    if len(arr) > 1:
        return __get_nippel_from_hex(val, 0)
    else:
        return 0


def get_second_nippel_from_hex(val):
    arr = get_nippel_array_from_hex(val)
    if len(arr) == 1:
        return __get_nippel_from_hex(val, 0)
    else:
        return __get_nippel_from_hex(val, 1)


def get_int_from_bit_list(bitlist):
    #example of this function:  Input:'0b1101000' --> Output: 104
    return int("".join(str(i) for i in bitlist), 2)


def get_roundet_float_value(val, digit):
    if isinstance(val, float):
        return float(format(val, f'.{digit}g'))
    elif isinstance(val, int):
        return int(val)
    else:
        return val


def get_array_as_string_reversed(value_that_should_be_flipped):
    return "".join(str(i)[2:].zfill(2) for i in reversed(value_that_should_be_flipped))


def get_array_as_string(value_arr):
    return "".join(str(i)[2:].zfill(2) for i in value_arr)


def hex_to_signed_integer(hexstr):
    hex_string_formated = format_hexstring_to_2digit_wellformated_hex_string(hexstr)
    return int.from_bytes(bytes.fromhex(hex_string_formated[2:]), byteorder="big", signed=True)


def format_hexstring_to_2digit_wellformated_hex_string(value):
    if str(value[0:2]).upper() == '0X':
        val_after_x = value[2:]
        if len(val_after_x) == 1:
            return f"0x{val_after_x.upper().zfill(2)}"
        else:
            return value
    else:
        return f"0x{value.upper().zfill(2)}"


def convert_hex_array_to_wellformed_hex_array(value_array):
    #example of this function:  Input:['0','A','3','4'] --> Output: ['0x00', '0x0A', '0x03', '0x04']
    well_formated_arr = []
    for data_item in value_array:
        well_formated_arr.append(format_hexstring_to_2digit_wellformated_hex_string(data_item))
    return well_formated_arr


def get_date_string(year,
                    month,
                    day,
                    hour=None,
                    minute=None,
                    seconds=None):
    if year is None:
        raise Exception("The attribute year must have a value and cannot be null")
    if month is None:
        raise Exception("The attribute month must have a value and cannot be null")
    if day is None:
        raise Exception("The attribute day must have a value and cannot be null")

    if year < 1:
        _logger.warning(f"The reported year (year = '{year}') does not correspond to an expected value. It is adjusted by the simulator accordingly to prevent an error")
        year = 1
    if year < 100:
        year = year + 2000

    if month < 1:
        month = 1

    if day < 1:
        day = 1

    if hour is not None or minute is not None or seconds is not None:
        if hour is None:
            hour = 0
        if minute is None:
            minute = 0
        if seconds is None:
            seconds = 0
        date_time = datetime(year, month, day, hour, minute, seconds)
        return date_time.strftime("%m/%d/%Y %H:%M")
    else:
        date_time = datetime(year, month, day)
        return date_time.strftime("%m/%d/%Y")


def get_bit_pattern(val, fillchar):
    mask = ''
    intp = range(1, val + 1)
    for i in intp:
        mask = mask + str(fillchar)
    return get_int_from_bit_list(mask)


def convert_to_boolean(value, default_if_value_is_empty):
    if not isinstance(default_if_value_is_empty, bool) and default_if_value_is_empty is not None:
        raise Exception(f"The default value {default_if_value_is_empty} is not a boolean")

    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        if value == "":
            return default_if_value_is_empty
        else:
            return value.lower() == 'true'
    elif isinstance(value, int):
        return value > 0
    elif isinstance(value, float):
        return value > 0.0
    elif value is None:
        return default_if_value_is_empty
    else:
        raise Exception(f"This type {type(value)} is not supported for conversion to boolean")


def get_formated_hexarray_from_stringarray(arr):
    data = []
    for i in arr:
        value_int = convert_hexstring_to_int(i)
        data.append(f"0x{value_int:02x}")
    return data


def reverse_string(string_value):
    return string_value[::-1]


def get_well_formatted_hex_array_from_string(string_with_hex_elements):
    #example of this function:  Input:'34F4' --> Output: ['0x34F4']
    arr_unformed = string_with_hex_elements.split()
    temp = [''.join(format_hexstring_to_2digit_wellformated_hex_string(item)) for item in arr_unformed]
    return temp


def convert_frame_string_to_int_array(convert_frame_string):
    #example of this function:  Input:'68 4E 4E 68' --> Output: [104, 78, 78, 104]
    arr_hex_str = convert_frame_string.split()
    arr_int = []
    for x in arr_hex_str:
        arr_int.append(convert_hexstring_to_int(x))
    return arr_int

def get_array_in_mbus_frame_structure(arr):
    return [''.join(item[2:].upper().zfill(2)) for item in arr]


def get_frame_string_from_int_array(arr_int):
    #example of this function:  Input:[104, 78, 78, 104] --> Output: '68 4E 4E 68'
    return_string = None
    if arr_int is not None:
        telegram_frame = [str(hex(i))[2:].upper().zfill(2) for i in arr_int]
        return_string = ' '.join(telegram_frame)
    else:
        return_string = None
    return return_string


def revers_frame(frame_as_string):
    arr = frame_as_string.split()
    arr.reverse()
    return ' '.join(arr)


def get_hex_array_from_int(value_int, zfill=None):
    #example of this function:  Input:5689 --> Output: ['0x1', '0x6', '0x3', '0x9']
    value_str = str(hex(value_int))
    arr = [hex(int(x, 16)) for x in value_str[2:]]
    if zfill is not None:
        while len(arr) < zfill:
            arr.insert(0,hex(0))
    return arr


def get_concatenated_hex_from_hex_array(arr_hex):
	concatenate = ''.join(format_hexstring_to_2digit_wellformated_hex_string(item)[2:] for item in arr_hex)
	return f'0x{concatenate}'


def byte_string_to_hex_array(raw_telegram):
    # example of this function:  Input:b'\x01\x03\x00\x03\x00\x065\xc8' --> Output: ['01', '03', '00', '03', '00', '06', '35', 'C8']
	array_hex = [byte for byte in raw_telegram]
	return [f'{byte:02X}' for byte in array_hex]


def get_int_array_from_hex_array (arr_hex):
    # example of this function:  Input:['0x68', '0x102', '0x102', '0x68', '0x08'] --> Output: [104, 258, 258, 104, 8]
    return [int(x[2:], 16) for x in arr_hex]