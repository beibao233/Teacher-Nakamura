from config.BFM_config import yaml_data


def wake_check(text, checklist):
    for i in checklist:
        if i.startswith("_"):
            if text.startswith(i.replace("_", "")):
                return True

        if text.startswith(yaml_data["Basic"]["WakeText"]+i):
            return True

