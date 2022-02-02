from saya import Including

from graia.saya import Saya, Channel
from graia.ariadne.model import Member
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image

from PIL import Image

from tool.callcheck import wake_check

import yaml
import requests
import random
import io


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
        ]}
})

with open('saya/InternetImageSender/member.yaml', 'r', encoding="utf-8") as f:
    file_data = f.read()
whitelist_data = yaml.load(file_data, Loader=yaml.FullLoader)


def get_kemomimi(qq):
    if not (qq in whitelist_data['MemberBlackList']):
        with io.BytesIO() as output:
            data = Image.save(
                requests.get(f"https://brx86.gitee.io/kemomimi/{str(random.randint(1, 581))}.jpg"
                             ), format="JPG").content
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
                Image(data)
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(f"您没有权限，抱歉！")]
            ))
