from graia.broadcast.interrupt import InterruptControl
from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication, Member
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import Group, GroupMessage
from graia.application.message.elements.internal import Plain, MessageChain, Voice_LocalFile, At

from config.BFM_config import yaml_data
from tool.removePunctuation import remPunc
from tool.TencentCloud.AI import talk

saya = Saya.current()
channel = Channel.current()
bcc = saya.broadcast
inc = InterruptControl(bcc)


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def AIchat(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    try:
        if message.getFirst(At).target == 2835692118 and not message.asDisplay().startswith("."):
            puremsg = remPunc(message.asDisplay().replace("@2835692118 ", "", 1))
            if talk(puremsg).find("腾讯") or talk(puremsg).find("小龙女"):
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain(f"你好 我是{yaml_data['Basic']['BotName']}")
                ]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain(f"" + talk(puremsg))
                ]))
    except IndexError:
        pass


