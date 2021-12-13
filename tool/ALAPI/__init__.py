from config.BFM_config import yaml_data

import requests


def censor_text(text):
    url = "https://v2.alapi.cn/api/censor/text"

    payload = f"token={yaml_data['AIAPI']['Token']}token&text={text}"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)

    return response

