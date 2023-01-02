import json
import logging
from os import path
from pathlib import Path


class StateService:
    def __init__(self):
        home_dir_ = str(Path.home())
        self.__state_file = home_dir_ + "/nmhillusion.state.py-send-template-mail.json"
        self.__makesure_existed_state_file()

        logging.info(f"home_dir: {home_dir_}")

    def __makesure_existed_state_file(self):
        if (not path.exists(self.__state_file)):
            # Writing to state file
            with open(self.__state_file, "w") as outfile_:
                outfile_.write(json.dumps({}))

    def __load_state(self):
        with open(self.__state_file, 'r') as openfile:
            # Reading from json file
            return json.load(openfile)

    def get_state(self, state_key_: str):
        _state = self.__load_state()
        if state_key_ in _state:
            return _state[state_key_]
        else:
            return None

    def save_state(self, data_: dict[str, any]):
        current_state_ = self.__load_state()

        for key_ in data_:
            current_state_[key_] = data_[key_]

        logging.info(f"save state: {current_state_}")

        with open(self.__state_file, "w") as outfile_:
            outfile_.write(json.dumps(current_state_))
