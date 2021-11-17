import json
import ast
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models

from config.BFM_config import yaml_data


def talk(text):
    try:
        cred = credential.Credential(yaml_data["TencentCloud"]["SecretId"],yaml_data["TencentCloud"]["SecretKey"])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

        req = models.ChatBotRequest()
        params = {
            "Query": text
        }
        req.from_json_string(json.dumps(params))

        resp = client.ChatBot(req)
        return ast.literal_eval(resp.to_json_string())["Reply"]
    except TencentCloudSDKException as err:
        return err


