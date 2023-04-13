from dataclasses import dataclass
from globalfunction import Globalfunction
import logger
import json
from nestedHtmlTable import NestedHtmlTable
from logger import get_header_open_tag, get_header_close_tag
import os


@dataclass
class ComPort:
    serial_port: str = "COM3"
    baud_rate: int = 19200
    data_bits: int = 8
    parity: str = "N"
    stop_bits: int = 2
    timeout: float = None
    xonxoff: bool = False
    rtscts: bool = False
    dsrdtr: bool = False
    write_timeout: float = None
    inter_byte_timeout: float = None
    exclusive: bool = None
    readout_break: float = 0.5

    def __init__(self):
        self._logger = logger.create_logger('ComPortCls')

    def get_settings(self):
        file_name = Globalfunction.get_filename_configport()
        try:
            config = Globalfunction.load_json_file(file_name)
            com_port = ComPort()
            com_port.serial_port = config["PortSettings"]["SerialPort"]
            com_port.baud_rate = config["PortSettings"]["BaudRate"]
            com_port.data_bits = config["PortSettings"]["DataBits"]
            com_port.parity = config["PortSettings"]["Parity"]
            com_port.stop_bits = config["PortSettings"]["StopBits"]
            com_port.xonxoff = False
            if config["PortSettings"]["Xonxoff"] == "1":
                com_port.xonxoff = True
            com_port.rtscts = False
            if config["PortSettings"]["Rtscts"] == "1":
                com_port.rtscts = True
            com_port.dsrdtr = False
            if config["PortSettings"]["Dsrdtr"] == "1":
                com_port.dsrdtr = True
            if str(config["PortSettings"]["InterByteTimeout"]).lower() != "none":
                com_port.inter_byte_timeout = float(
                    config["PortSettings"]["InterByteTimeout"])
            else:
                com_port.inter_byte_timeout = None
            if str(config["PortSettings"]["WriteTimeout"]).lower() != "none":
                com_port.write_timeout = float(
                    config["PortSettings"]["WriteTimeout"])
            else:
                com_port.write_timeout = None
            if str(config["PortSettings"]["Timeout"]).lower() != "none":
                com_port.timeout = float(config["PortSettings"]["Timeout"])
            else:
                com_port.timeout = None
            if str(config["PortSettings"]["Exclusive"]).lower() != "none":
                com_port.exclusive = bool(config["PortSettings"]["Exclusive"])
            else:
                com_port.exclusive = None

            com_port.readout_break = float(
                config["PortSettings"]["ReadoutBreak"])

        except Exception as ex:
            msg = f"There is a general problem reading the serialPort configuration, \
                    which is defined in the file '{file_name}'. Please try to define \
                    the serialPort settings via the API and execute the process again. \
                    Error: '{ex}'"
            self._logger.error(msg)
            raise Exception(msg) from ex
        return com_port

    def save_settings(self, file_name):
        try:
            port_detail = {}
            port_detail["BaudRate"] = self.baud_rate
            port_detail["SerialPort"] = self.serial_port
            port_detail["DataBits"] = self.data_bits
            port_detail["Parity"] = self.parity
            port_detail["StopBits"] = self.stop_bits
            port_detail["Xonxoff"] = self.xonxoff
            port_detail["Rtscts"] = self.rtscts
            port_detail["Dsrdtr"] = self.dsrdtr
            if str(self.inter_byte_timeout).lower() != "none":
                port_detail["InterByteTimeout"] = self.inter_byte_timeout
            else:
                port_detail["InterByteTimeout"] = "None"

            if str(self.write_timeout).lower() != "none":
                port_detail["WriteTimeout"] = self.write_timeout
            else:
                port_detail["WriteTimeout"] = "None"

            if str(self.write_timeout).lower() != "none":
                port_detail["Exclusive"] = self.exclusive
            else:
                port_detail["Exclusive"] = "None"
            port_detail["ReadoutBreak"] = self.readout_break

            if str(self.timeout).lower() != "none":
                port_detail["Timeout"] = self.timeout
            else:
                port_detail["Timeout"] = "None"

            json_object = {}
            json_object["PortSettings"] = port_detail

            Globalfunction.create_new_file_or_overwrite_file_if_exist(
                file_name, json.dumps(json_object, indent=4))
        except Exception as ex:
            msg = f"Save file '{file_name}' Error: '{ex}'"
            self._logger.error(msg)
            raise Exception(msg) from ex
        


    def get_port_overview_in_html(self):
        nested_html_table = NestedHtmlTable("Description","Value")
        nested_html_table.add_title("Configuration port settings")
        comPort = self.get_settings()

        file_name = Globalfunction.get_filename_configport()
        header_open = get_header_open_tag("", "")
        if os.path.exists(file_name):
            nested_html_table.add_info("Serial port",comPort.serial_port)
            nested_html_table.add_info("Baudrate",comPort.baud_rate)
            nested_html_table.add_info("Databits",comPort.data_bits)
            nested_html_table.add_info("Parity",comPort.parity)
            nested_html_table.add_info("Stopbits",comPort.stop_bits)
            nested_html_table.add_info("Timeout",comPort.timeout)
            nested_html_table.add_info("Xon xoff",comPort.xonxoff)
            nested_html_table.add_info("Rtscts",comPort.rtscts)
            nested_html_table.add_info("Dsrdtr",comPort.dsrdtr)
            nested_html_table.add_info("Write timeout",comPort.write_timeout)
            nested_html_table.add_info("Inter byte timeout",comPort.inter_byte_timeout)
            nested_html_table.add_info("Exclusive",comPort.exclusive)
            nested_html_table.add_info("Readout break",comPort.readout_break)
        else:
            nested_html_table.add_info("Warning", "The port settings do not exist. Execute the appropriate API call to define the communication settings!")
        header_close = get_header_close_tag("")
        return f"{header_open}{nested_html_table.get_html_as_string()}{header_close}"