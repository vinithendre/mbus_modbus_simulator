from modbusRequest import ModbusRequest
from modbusMaster import ModbusMaster
from comPort import ComPort
from globalfunction import Globalfunction
import logger


_logger = logger.create_logger('Bulk_devco')
TIMEOUT = 3

def log(msg, pint_on_screen=False):
    _logger.info(msg)
    if pint_on_screen is True:
        print(msg)
    

def set_modbus_command(slave_address, function_code, address_register_of_not_autozero, value, count_register=None):
    modbusMaster = ModbusMaster()
    modbusRequest = ModbusRequest(None)
    modbusRequest.slave_address = slave_address
    modbusRequest.function_code = function_code
    modbusRequest.address_register = address_register_of_not_autozero
    modbusRequest.count_register = count_register
    modbusRequest.value = value
    return modbusMaster.send_to_slave(slave_address = modbusRequest.slave_address, function_code=modbusRequest.function_code, address_register=modbusRequest.address_register, count_register=modbusRequest.count_register, value=modbusRequest.value)


def set_baudrate_on_device(slave_address: int, baudrate: int):
    rsp_frame = set_modbus_command(slave_address=slave_address, function_code=6, address_register_of_not_autozero=1, value=get_baudrate_value(baudrate))
    ok = len(rsp_frame) > 1
    if ok:
        log(f"The baudrate of the device with the slave address '{slave_address}' could be successfully changed  to '{baudrate}'")
    else:
        log(f"Error: The baudrate of the device with the slave address '{slave_address}' could not be changed to '{baudrate}'")
    return ok        


def set_frameformat_on_device(slave_address: int, parity: str, stop_bit: int):
    rsp_frame = set_modbus_command(slave_address=slave_address, function_code=6, address_register_of_not_autozero=2, value=get_frameformat_value(parity, stop_bit))
    ok = len(rsp_frame) > 1
    if ok:
        log(f"The frame format of the device with the slave address '{slave_address}' could be successfully changed to parity '{parity}' and stop bit '{stop_bit}'")
    else:
        log(f"Error: The frame format of the device with the slave address '{slave_address}' could be successfully changed to parity '{parity}' and stop bit '{stop_bit}'")
    return ok     


def get_frameformat_value(parity, stop_bit: int):
    return_value = -1
    if parity.upper() == "E" and stop_bit == 1:
        return_value = 0
    elif parity.upper() == "O" and stop_bit == 1:
        return_value = 1
    elif parity.upper() == "N" and stop_bit == 1:
        return_value = 2
    elif parity.upper() == "N" and stop_bit == 2:
        return_value = 3
    else:
        log(f"parity {parity} and stop_bit {stop_bit} is not supported. So the slave will be configurated with the default values")
        return_value = 0
    return return_value


def set_baudrate_settings(baudrate: int, timeout: int, parity: str, stop_bit: int):
    comPort = ComPort()
    comPort.serial_port = "/dev/ttyUSB0"
    comPort.baud_rate = baudrate
    comPort.data_bits = 8
    comPort.parity = parity
    comPort.stop_bits = stop_bit
    comPort.timeout = timeout
    comPort.xonxoff = False
    comPort.rtscts = False
    comPort.dsrdtr = False
    comPort.write_timeout = None
    comPort.inter_byte_timeout = None
    comPort.exclusive = None
    comPort.readout_break = 0.5
    comPort.save_settings(Globalfunction.get_filename_configport())


def client_exists(slave_address: int):
    modbusMaster = ModbusMaster()
    modbusRequest = ModbusRequest(None)
    modbusRequest.slave_address = slave_address
    modbusRequest.function_code = 3
    modbusRequest.address_register = 1
    modbusRequest.count_register = 6

    rsp_frame = modbusMaster.send_to_slave(slave_address = modbusRequest.slave_address, function_code=modbusRequest.function_code, address_register=modbusRequest.address_register, count_register=modbusRequest.count_register)
    return len(rsp_frame) > 3


def get_baudrate_value(baudrate: int):
    return_value = None
    match baudrate:
        case 9600:
            return_value = 1
        case 19200:
            return_value = 2
        case 38400:
            return_value = 3
        case 57600:
            return_value = 3
        case _:
            return_value = 2
    return return_value


def get_data_frame_formats():
    return  [["E",1], ["O",1], ["N",1], ["N",2]]


def get_baudrates():
    # return [300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400]
    return [9600, 19200, 38400, 57600]


def clear_log():
    Globalfunction.create_new_file_or_overwrite_file_if_exist(Globalfunction.get_filename_log(), '')


def device_accessible(slave_address):
    device_found = False
    for data_frame_format in get_data_frame_formats():
        for baudrate in get_baudrates():
            parity = data_frame_format[0]
            stop_bit = data_frame_format[1]
            set_baudrate_settings(baudrate, TIMEOUT, parity, stop_bit)
            log(f"Check with '{slave_address}'  baudrate:'{baudrate}', parity: '{parity}', stop bits:'{stop_bit}'")
            if client_exists(slave_address) is True:
                log (f"A Modbus device with the slave address '{slave_address}' can be reached with settings: baudrate:'{baudrate}', parity: '{parity}', stop bits:'{stop_bit}'", True)
                device_found = True
                break
        if device_found is True:
            break
    if device_found is False:
        msg = f"No device could be found at slave address {slave_address}"
        log(msg, True)
    return device_found


def get_address_ranges():
    arr = []
    for i in range(1,255):
        arr.append(i)
    return arr



def configure_device(slave_addr, baudrate, parity, stop_bit):
    device_1 = device_accessible(slave_addr)
    status_Test = device_1
    if status_Test is True:
        status_Test = status_Test and set_baudrate_on_device(slave_addr, baudrate)
        status_Test = status_Test and device_accessible(slave_addr)
        if status_Test is True:
            status_Test = status_Test and set_frameformat_on_device(slave_addr, parity, stop_bit)
            status_Test = status_Test and device_accessible(slave_addr)
    if status_Test is True:
        log(f"The device with the address '{slave_addr}' was successfully change to baudrate '{baudrate}', parity '{parity}' and stop bit '{stop_bit}'")
    else:
        log(f"Error: The device with the address '{slave_addr}' could not successfully change to baudrate '{baudrate}', parity '{parity}' and stop bit '{stop_bit}'")
        

def scan_device():
    for slave_addr in get_address_ranges():
       device_accessible(slave_addr)





# Main programm
# *************************************************************************************


clear_log()
# configure_device(10, 19200, "E", 1)
# configure_device(10, 9600, "N", 2)
scan_device()




