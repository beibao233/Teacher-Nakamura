from graia.saya import Saya, Channel
from graia.ariadne.model import Member
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, At

from config.BFM_config import yaml_data
from tool.TencentCloud.AI import talk
from saya import Including

# Self-Including
readme = Including(author=None, group="角色功能", functions={
            "AIchat": {
                "describe": "对话",
                "show": True,
                "keys": [
                    "_AT"
                ]
            }
        })


saya = Saya.current()
channel = Channel.current()
bcc = saya.broadcast


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def AIchat(app: Ariadne, group: Group, message: MessageChain, member: Member):
    try:
        if message.getFirst(At).target == 2835692118:
            puremsg = message.asDisplay().replace("@2835692118 ", "", 1)
            if "腾讯" in talk(puremsg):
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain(f"你好 我是{yaml_data['Basic']['BotName']}")
                ]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain(f"" + talk(puremsg))
                ]))
    except IndexError:
        pass
