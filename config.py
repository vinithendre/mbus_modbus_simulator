import json
from dataclasses import dataclass
from globalfunction import Globalfunction
import logger
import constants as const


@dataclass
class Config:

    def __init__(self):
        self._logger = logger.create_logger('Config_Cls')


    def get_simulator_mode(self):
        file_name = Globalfunction.get_filename_config()
        try:
            section = "Protocol"
            config = Globalfunction.load_json_file(file_name)
            return config[section]
        except Exception as ex:
            msg = f"Read file '{file_name}' failled! Error: '{ex}'. May to execute \
                    API methode to setSimulatorMode"
            self._logger.error(msg)
            raise Exception(msg) from ex
        

    def its_modbus(self):
        val_prot = self.get_simulator_mode()
        if val_prot.lower() == const.CONFIG_SIMMULATORMODE_MODBUS.lower():
            return True
        elif val_prot.lower() == const.CONFIG_SIMMULATORMODE_MBUS.lower():
            return False
        else:
            raise Exception(f"The value {val_prot} is wrong: Valid value are: '{self.get_allowed_simulator_mode()}'")


    def get_allowed_simulator_mode(self):
        return [const.CONFIG_SIMMULATORMODE_MODBUS, const.CONFIG_SIMMULATORMODE_MBUS]


    def save_simulator_mode(self, simulator_mode):
        try:
            if simulator_mode in self.get_allowed_simulator_mode():
                file_fame = Globalfunction.get_filename_config()
                sim_mode = {}
                sim_mode["Protocol"] = simulator_mode
                Globalfunction.create_new_file_or_overwrite_file_if_exist(
                    file_fame, json.dumps(sim_mode, indent=4))
            else:
                msg = f"The value '{simulator_mode}' is not allowed. The following \
                        definitions are allowed: '{Globalfunction.get_filename_config()}'"
                self._logger.error(msg)
        except Exception as ex:
            msg = f"Save file '{file_fame}' Error: '{ex}'"
            self._logger.error(msg)
            raise Exception(msg) from ex


    def simulator_says_hello(self):
        greetings = "Hello, I am the simulator for modbus and mbus"
        if self.its_modbus():
            mode = "modbus"
        else:
            mode = "mbus"
        greetings = f"{greetings} and I am configured now as a {mode}"
        return greetings
