from pathlib import Path
from os import path
import json


class StateService:
    def __init__(self):
        home_dir_ = str(Path.home())
        self.__state_file = home_dir_ + \
            "/nmhillusion.state.py-send-template-mail.json"
        self.__makesure_existed_state_file()

    def __makesure_existed_state_file(self):
        if (not path.exists(self.__state_file)):
            # Writing to state file
            with open(self.__state_file, "w") as outfile_:
                outfile_.write(json.dumps({}))

    def load_state(self):
        with open(self.__state_file, 'r') as openfile:
            # Reading from json file
            return json.load(openfile)

    def save_state(self, data_: dict[str, any]):
        with open(self.__state_file, "w") as outfile_:
            outfile_.write(json.dumps(data_))


state_ = StateService()

data_old_state_ = state_.load_state()
print("old state: ", data_old_state_)

data_old_state_ = {
  "data": {
    "excel": {
      "start_path": "~/codespace/nmhillusion/data/excel"
    }
  }
}

state_.save_state(data_old_state_)

print("new state: ", state_.load_state())

