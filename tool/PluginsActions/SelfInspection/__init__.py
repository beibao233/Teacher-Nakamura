from config.BFM_config import yaml_data

import os


def inspection(plugin_name, plugin_group, plugin_functionlist, plugin_author):
    if plugin_name in yaml_data["saya"]:
        if (
            plugin_group in yaml_data["saya"][plugin_name] and
            plugin_functionlist in yaml_data["saya"][plugin_name] and
            plugin_author in yaml_data["saya"][plugin_name]
        ):
            return True
        else:
            return False
    else:
        return False


def remove_inspection(ignore=None):
    if ignore is None:  # 初始化ignore列表
        ignore = ["__init__.py", "__pycache__"]

    data = yaml_data["Saya"].keys()  # 获取保存的插件名称数据

    real = []  # 新建现实插件名称数据

    for module in os.listdir("saya"):  # 获取现实存在的插件名称
        if module in ignore:
            continue
        if os.path.isdir(module):
            real.append(module)
        else:
            real.append(module.split('.')[0])

    for name in data:
        if not (name in real):  # 判断是否存在 如果不存在删除
            del yaml_data["Saya"][name]
