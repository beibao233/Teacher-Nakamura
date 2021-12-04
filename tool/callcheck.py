from config.BFM_config import yaml_data


def wake_check(text, checklist):
    for i in checklist:
        if i.startswith("_"):
            if text.startswith(yaml_data["Basic"]["WakeText"]):
                return True

        if i == text.replace(yaml_data["Basic"]["WakeText"], "")\
                and text.startswith(yaml_data["Basic"]["WakeText"]):
            return True

