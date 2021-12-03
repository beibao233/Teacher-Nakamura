from config.BFM_config import yaml_data


def wake_check(text, checklist):
    for i in checklist:
        if text.replace(yaml_data["Basic"]["WakeText"], "") == i and text.startswith(yaml_data["Basic"]["WakeText"]):
            return True
