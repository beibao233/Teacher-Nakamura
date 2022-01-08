# from saya import Including

import yaml
import os
import atexit

global user_data


# readme = Including(author=None, group="后端功能", functions={})

path = os.path.abspath(os.path.dirname(__file__))


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


class UserRegistryError(Exception):
    """
        When User already registred
        This error will raise
    """
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message

    __module__ = 'builtins'


class UserUnregisteredError(Exception):
    """
        When User didn't registry
        This error will raise
    """
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message

    __module__ = 'builtins'


if not os.path.exists(f'{path}/data.yaml'):
    print('未检测到用户数据文件！正在创建！')
    with open(f'{path}/data.yaml', 'x', encoding="utf-8") as f:
        print("创建成功！")
    user_data = {}
else:
    with open(f'{path}/data.yaml', 'r', encoding="utf-8") as f:
        file_data = f.read()
    user_data = yaml.load(file_data, Loader=yaml.FullLoader)


def register(indicator):
    """
    Registry User ID and Initialization User Data Profile
    :param indicator: A never change indicator valve
    :return:
    """
    if indicator in user_data:
        raise UserRegistryError("User already in data.")
    else:
        uid = len(user_data) + 1
        user_data[indicator] = {"UID": uid}


def data_save(indicator, key, data):
    """
    Save user data in profile by key
    :param indicator: A never change indicator valve
    :param key: A valve to get data
    :param data: What you wanna to store
    :return:
    """
    try:
        register(indicator)
        raise UserUnregisteredError("User isn't registry. Register First Before Use.")
    except UserRegistryError:
        user_data[indicator][key] = data


def data_del(indicator, key):
    """
    Save user data in profile by key
    :param indicator: A never change indicator valve
    :param key: A valve to get data
    :return:
    """
    try:
        register(indicator)
        raise UserUnregisteredError("User isn't registry. Register First Before Use.")
    except UserRegistryError:
        del user_data[indicator][key]


def indicator_get_data(indicator, key=None):
    """
    Get data from indicator
    Key is optional, If you di
    :param indicator:
    :param key:
    :return:
    """
    if key is None:
        return user_data[indicator]
    else:
        return user_data[indicator][key]


def get_data():
    """
    get data
    :return: data
    """
    return user_data

@atexit.register
def save_userdata():
    with open(f'{path}/data.yaml', 'w', encoding="utf-8") as f:
        yaml.dump(user_data, f, allow_unicode=True, Dumper=NoAliasDumper)
