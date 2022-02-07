from config.BFM_config import yaml_data


def wake_check(text, checklist):
    for i in checklist:
        if i.startswith("_"):
            if i.replace("_", "") == text:
                return True

        for _ in yaml_data["Basic"]["WakeText"]:
            if i == text.replace(_, "")\
                    and text.startswith(_):
                return True

