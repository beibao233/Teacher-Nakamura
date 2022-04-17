from graia.saya import Saya, Channel
from graia.ariadne.model import Member
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, At

import aiohttp
import ast
import json
import aiohttp

from saya import Including
from tool.callcheck import wake_check_var

# Self-Including
readme = Including(author=None, group="查询功能", functions={
            "BC": {
                "describe": "B站用户查询",
                "show": True,
                "keys": [
                    "UID",
                    "B站"
                ]
            }
        })


saya = Saya.current()
channel = Channel.current()

async def user(uid):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.bilibili.com/x/relation/stat?vmid={uid}&jsonp=jsonp") as response:
                r = await response.text()
            async with session.get(f"https://api.bilibili.com/x/space/acc/info?mid={uid}") as response:
                rr = await response.text()

            follow = ast.literal_eval(r)["data"]["following"]
            follower = ast.literal_eval(r)["data"]["follower"]
            name = json.loads(rr)["data"]["name"]
            sex = json.loads(rr)["data"]["sex"]
            sign = json.loads(rr)["data"]["sign"]
            msg = f"\n{name}:\n签名：{sign}\n性别：{sex}\n关注：{str(follow)}人\n粉丝：{str(follower)}人"
            if uid == "208259":
                msg = msg + "\n叔叔我啊, 可要生气了。"
    except KeyError:
        msg = "查无此人！"
    return msg


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jrrpIn(app: Ariadne, group: Group, message: MessageChain, member: Member):
    data = wake_check_var(message.asDisplay(), readme.functions["BC"]["keys"])
    if data is not False:
        await app.sendGroupMessage(group, MessageChain.create(
            [
                At(member.id), Plain(await user(data.strip()))
            ]))