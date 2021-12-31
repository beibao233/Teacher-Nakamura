from saya import Including

import yaml
import os
import atexit

global user_data


readme = Including(author=None, group="后端功能", functions={})

# indicator stand for qq number


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


if not os.path.exists('saya/MemberDataSaveControl/data.yaml'):
    print('未检测到用户数据文件！正在创建！')
    with open('saya/MemberDataSaveControl/data.yaml', 'w', encoding="utf-8") as f:
        print("创建成功！")
else:
    with open('saya/MemberDataSaveControl/data.yaml', 'r', encoding="utf-8") as f:
        file_data = f.read()
    user_data = yaml.load(file_data, Loader=yaml.FullLoader)


def register(indicator):
    if indicator in user_data:
        raise("UserRegistryError", "User already in data.")
    else:
        user_data[indicator]["UID"] = len(user_data) + 1


def user_save(indicator, key, data):
    try:
        register(indicator)
    except "UserRegistryError":
        user_data[indicator][key] = data
    raise("UserUnregisteredError", "User isn't registry. Register First Before Use.")


@atexit.register
def save_config():
    with open('saya/MemberDataSaveControl/data.yaml', 'w', encoding="utf-8") as f:
        print("创建成功！")
        yaml.dump(user_data, f, allow_unicode=True, Dumper=NoAliasDumper)
