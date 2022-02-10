from config.BFM_config import yaml_data


def key_list_format(text, checklist):
    for i in checklist:
        if i.startswith("_"):
            if i.replace("_", "") == text:
                return [True, i]
    return [False]


def wake_check(text, checklist):
    if key_list_format(text, checklist)[0]:
        return True

    for i in checklist:
        for _ in yaml_data["Basic"]["WakeText"]:
            if i == text.replace(_, "") and text.startswith(_):
                return True


def wake_check_var(text, checklist):
    cache4nowt = key_list_format(text, checklist)
    if cache4nowt[0]:
        result = text.replace(cache4nowt[1], "", 1).strip()
        return result

    for i in checklist:
        for _ in yaml_data["Basic"]["WakeText"]:
            if text.replace(_, "").startswith(i) and text.startswith(_):
                result = text.replace(i, "", 1).replace(_, "", 1)
                return result
    return False
