﻿from saya import Including

from graia.saya import Saya, Channel
from graia.ariadne.model import Member
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image

from PIL import Image as Images

from tool.callcheck import wake_check

import yaml
import requests
import random
import io
import os


saya = Saya.current()
channel = Channel.current()

readme = Including(author=None, group="基础功能", functions={
    "xhl": {
        "describe": "随机小狐狸表情包",
        "show": True,
        "keys": [
            "xhl",
            "gxhl",
            "hl",
            "狐狸",
            "小狐狸"
        ]},
    "xdn": {
        "describe": "随机小豆泥表情包",
        "show": True,
        "keys": [
            "xdn",
            "gxdn",
            "dn",
            "豆泥",
            "小豆泥"
        ]}
})

# Get Whitelist data from file.
with open('saya/InternetImageSender/member.yaml', 'r', encoding="utf-8") as f:
    file_data = f.read()
whitelist_data = yaml.load(file_data, Loader=yaml.FullLoader)

# Get LocalImagesList and make it useful.
with open('saya/InternetImageSender/images.yaml', 'r', encoding="utf-8") as f:
    file_data = f.read()
images_name_data = yaml.load(file_data, Loader=yaml.FullLoader)

Key2Images = {}

for _ in images_name_data["NameOTImage"]:
    Key2Images[_] = images_name_data["NameOTImage"][_]["KeyFrom"]


def image_to_byte_array(image: Images):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def get_kemomimi(qq):
    if not (qq in whitelist_data['MemberBlackList']):
        data = Images.open(io.BytesIO(
                requests.get(f"https://brx86.gitee.io/kemomimi/{str(random.randint(1, 581))}.jpg"
                             ).content))
        data = image_to_byte_array(data)
        return data
    else:
        return False


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def xhl(
        app: Ariadne,
        group: Group,
        member: Member,
        saying: MessageChain
):
    if wake_check(saying.asDisplay(), readme.functions["xhl"]["keys"]):
        data = get_kemomimi(member.id)
        if data is not False:
            await app.sendGroupMessage(group, MessageChain.create([
                Image(data_bytes=data)
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(f"您没有权限，抱歉！")]
            ))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def send_image_from_group_of_file(
        app: Ariadne,
        group: Group,
        member: Member,
        saying: MessageChain
):
    for _ in Key2Images:
        if not (member.id in whitelist_data['MemberBlackList']):
            if wake_check(saying.asDisplay(), readme.functions[Key2Images[_]]["keys"]):
                images_number = len(os.listdir(f"{__file__}/{_}")) - 1
            await app.sendGroupMessage(group, MessageChain.create([
                Image(file=f"{__file__}/{_}/{random.randint(1,images_number)}.JPG")
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(f"您没有权限，抱歉！")]
            ))
            break
