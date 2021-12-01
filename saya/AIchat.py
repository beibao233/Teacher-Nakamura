from graia.broadcast.interrupt import InterruptControl
from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication, Member
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import Group, GroupMessage
from graia.application.message.elements.internal import Plain, MessageChain, Voice_LocalFile, At

from config.BFM_config import yaml_data
from tool.TencentCloud.AI import talk

# Self-Including
_author = None
_group = "角色功能"
_functions = {
    "AIchat": {
        "describe": "对话",
        "show": True,
        "keys": [
            "_AT"
        ]
    }
}

saya = Saya.current()
channel = Channel.current()
bcc = saya.broadcast
inc = InterruptControl(bcc)


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def AIchat(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
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


