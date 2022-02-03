from config.BFM_config import yaml_data, save_config

import importlib
import os


class Including:
    def __init__(self, author: None or str, group: str, functions: dict):
        self.author = author
        self.group = group
        self.functions = functions


readme = Including(author=None, group="后端功能", functions={})


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


def inspection_check(plugin_name, plugin_group, plugin_functions_list, plugin_author):
    """
    Check plugins are ready write readme or not
    :param plugin_name: the file name without extension
    :param plugin_group: the group of plugin in
    :param plugin_functions_list: the functions of plugin have and their readme
    :param plugin_author: the author of the plugins
    :return: the result of plugin readme have or not
    """
    try:
        if plugin_name in yaml_data["saya"]:
            if (
                plugin_group in yaml_data["saya"][plugin_name] and
                plugin_functions_list in yaml_data["saya"][plugin_name] and
                plugin_author in yaml_data["saya"][plugin_name]
            ):
                return True
    except KeyError:
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

    if plugin_author is None:
        plugin_author = "Include"

    for _ in plugin_functions_list.keys():
        if not plugin_functions_list[_]["show"] is False or plugin_group == "后端功能":

            plugin_data = {
                "Group": plugin_group,
                "Functions": plugin_functions_list,
                "Author": plugin_author
            }

            yaml_data["Saya"][plugin_name] = plugin_data
            del plugin_data
        save_config(yaml_data)


for plugin in real_plugins():
    current = importlib.import_module("saya."+plugin)
    data = current.readme
    # Check the plugins readme
    if not inspection_check(plugin, data.group, data.functions, data.author):
        add_plugin_readme(plugin, data.group, data.functions, data.author)
        remove_readme()
