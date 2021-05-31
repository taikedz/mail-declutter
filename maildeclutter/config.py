import os
import copy
import getpass

import yaml


def __get_password(password):
    if password is None:
        password = os.getenv("MAIL_DECLUTTER_PASS", None)

    if password is None:
        password = getpass.getpass("Enter password: ")

    return password


def load_config():
    with open("mail_declutter_config.yaml") as fh:
        config = yaml.safe_load(fh)

    config = XPathConfig(config)

    config.set("/credentials/password", __get_password(config["/credentials/password"]) )

    return config


class XPathConfig:
    
    def __init__(self, data):
        self.data = data


    def __split_path(self, path):
        path_steps = path.split("/")
        if path_steps[0] == '':
            path_steps = path_steps[1:]

        return path_steps


    def __getitem__(self, key, default=None):
        return self.get(key, default)


    def __setitem__(self, key, value):
        return self.set(key, value)


    def get(self, path, default=None):
        path_steps = self.__split_path(path)
        data_ref = self.data

        for step in path_steps[:-1]:
            data_ref = data_ref.get(step, {})

        data_ref = copy.deepcopy(data_ref.get(path_steps[-1]))

        return data_ref


    def set(self, path, value):
        path_steps = self.__split_path(path)
        data_ref = self.data

        for step in path_steps[:-1]:
            if data_ref.get(step) is None:
                data_ref[step] = {}

            data_ref = data_ref[step]

        data_ref[path_steps[-1]] = value
