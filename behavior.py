
from dataclasses import dataclass
from dataFile import DataFile
from globalfunction import Globalfunction
import json
import logger


@dataclass
class Behavior:

    section = "ResponseBehavior"

    def __init__(self):
        self._logger = logger.create_logger('_Behavior_')

    def get_response_behavior(self):
        file_name = Globalfunction.get_filename_behavior()
        try:
            behavior_val = Globalfunction.load_json_file(file_name)
            return behavior_val[Behavior.section]
        except Exception as ex:
            msg = f"Read file '{file_name}' failled! Error: '{ex}'. \
                    May to execute API methode to responseBehavior"
            self._logger.warning(msg)
            return 0


    def set_response_behavior(self, value):
        try:
            allowed_value = range(-1, 300001, 1)
            if value in allowed_value:
                file_name = Globalfunction.get_filename_behavior()
                data_structure = {}
                data_structure[Behavior.section] = value
                Globalfunction.create_new_file_or_overwrite_file_if_exist(file_name,
                                                                   json.dumps(data_structure, indent=4))
            else:
                msg = f"The value '{value}' is not allowed. Only the following \
                        values are allowed: '{allowed_value}'"
                self._logger.error(msg)
        except Exception as ex:
            msg = f"Save file '{file_name}' Error: '{ex}'"
            self._logger.error(msg)
            raise Exception(msg) from ex
