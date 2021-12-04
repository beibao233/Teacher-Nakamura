from graia.broadcast.interrupt import InterruptControl
from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication, Member
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import Group, GroupMessage
from graia.application.message.elements.internal import Plain, MessageChain, At

from tool.callcheck import wake_check
from config.BFM_config import yaml_data
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


def help_msg(msg_start="帮助列表:"):
    groups = {}

    for _ in yaml_data["Saya"].keys():
        if yaml_data["Saya"][_]["Group"] in groups:
            groups[yaml_data["Saya"][_]["Group"]].append(_)
        else:
            groups[yaml_data["Saya"][_]["Group"]] = [_]

    for _ in groups:
        if not _ == "后端功能":
            msg_start += f"\n——————{_}——————"
            for gs in groups[_]:
                for _ in yaml_data["Saya"][gs]['Functions']:
                    if yaml_data["Saya"][gs]['Functions'][_]["show"]:
                        if yaml_data["Saya"][gs]['Functions'][_]["keys"][0].startswith("_"):
                            if yaml_data["Saya"][gs]['Functions'][_]["keys"][0] == "_AT":
                                msg_start += f"\n@{yaml_data['Basic']['BotName']}: " + \
                                            yaml_data["Saya"][gs]['Functions'][_]["describe"]
                            else:
                                msg_start += "\n" +\
                                             yaml_data["Saya"][gs]['Functions'][_]["keys"][0].replace("_", "") + ": " + \
                                             yaml_data["Saya"][gs]['Functions'][_]["describe"]
                        else:
                            msg_start += "\n" + yaml_data["Basic"]["WakeText"] + \
                                        yaml_data["Saya"][gs]['Functions'][_]["keys"][0] + ": " + \
                                        yaml_data["Saya"][gs]['Functions'][_]["describe"]
    return msg_start


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def help_handler(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    if wake_check(message.asDisplay().strip(), readme.functions["help"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain(f"\n" + help_msg())]
        ))
