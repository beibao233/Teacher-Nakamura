from config.BFM_config import yaml_data


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
