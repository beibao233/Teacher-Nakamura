from graia.broadcast.interrupt import InterruptControl
from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication, Member
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import Group, GroupMessage
from graia.application.message.elements.internal import Plain, MessageChain, At

from tool.callcheck import wake_check
from saya import Including

# Self-Including
readme = Including(author=None, group="基础功能", functions={
            "help": {
                "describe": "获取帮助",
                "show": True,
                "keys": [
                    "help",
                    "救命",
                    "帮助",
                    "bg"
                ]
            }
        })


saya = Saya.current()
channel = Channel.current()
bcc = saya.broadcast
inc = InterruptControl(bcc)


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def helpHandler(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    if wake_check(message.asDisplay().strip(), _functions["help"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain(f"\n帮助列表：\n——————角色功能——————\n@机器人：对话\n——————基础功能——————\n.jrrp 今日人品"
                                 f"\n.ntgm 逆天改命\n.ci 签到")]
        ))
