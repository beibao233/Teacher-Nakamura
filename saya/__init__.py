from config.BFM_config import yaml_data

import os

# Self-Including
_author = None
_group = "后端功能"
_functions = {}


def real_plugins():
    """
    Return plugins are load
    :return: list of plugins are load
    """

    real = []  # 新建现实插件名称数据

    for module in os.listdir("saya"):  # 获取现实存在的插件名称
        if module == "__pycache__":
            continue
        if os.path.isdir(module):
            real.append(module)
        else:
            real.append(module.split('.')[0])

    return real


def inspection(plugin_name, plugin_group, plugin_functions_list, plugin_author):
    """
    Check plugins are ready write readme or not
    :param plugin_name: the file name without extension
    :param plugin_group: the group of plugin in
    :param plugin_functions_list: the functions of plugin have and their readme
    :param plugin_author: the author of the plugins
    :return: the result of plugin readme have or not
    """
    if plugin_name in yaml_data["saya"]:
        if (
            plugin_group in yaml_data["saya"][plugin_name] and
            plugin_functions_list in yaml_data["saya"][plugin_name] and
            plugin_author in yaml_data["saya"][plugin_name]
        ):
            return True
        else:
            return False
    else:
        return False


def remove_readme():
    """
    Remove readme of not exist plugins
    """
    data = yaml_data["Saya"].keys()  # 获取保存的插件名称数据

    real = real_plugins()

    for name in data:
        if not (name in real):  # 判断是否存在 如果不存在删除
            del yaml_data["Saya"][name]


def add_plugin_readme(plugin_name, plugin_group, plugin_functions_list, plugin_author):
    """
    add plugin readme
    :param plugin_name: the file name without extension
    :param plugin_group: the group of plugin in
    :param plugin_functions_list: the functions of plugin have and their readme
    :param plugin_author: the author of the plugins
    :return:
    """
    data = {
        "Group": plugin_group,
        "Functions": plugin_functions_list,
        "Author": plugin_author
    }

    yaml_data["Saya"][plugin_name] = data


for plugin in real_plugins():
    current = __import__(plugin)
