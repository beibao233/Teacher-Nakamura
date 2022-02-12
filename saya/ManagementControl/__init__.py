from graia.saya import Saya, Channel
from graia.ariadne.model import Member
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, At

from tool.callcheck import wake_check_var, wake_check

from config.BFM_config import yaml_data
from saya import Including

saya = Saya.current()
channel = Channel.current()

# Self-Including
readme = Including(author=None, group="管理功能", functions={
    "appointment": {
        "describe": f"添加一个人为{yaml_data['Basic']['BotName']}管理",
        "show": True,
        "keys": [
            "appo",
            "appoint",
            "adda",
            "任命"
        ]},
    "clear": {
        "describe": f"清屏",
        "show": True,
        "keys": [
            "clear",
            "清屏"
        ]},

})


def admins():
    admin = yaml_data["Basic"]["Permission"]["Admin"]
    admin.append(yaml_data["Basic"]["Permission"]["Master"])
    return admin


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def appointment(
        app: Ariadne,
        group: Group,
        member: Member,
        saying: MessageChain
):
    data = wake_check_var(saying.asDisplay(), readme.functions["appointment"]["keys"])
    if data is str and member.id in admins():
        if data != "":
            yaml_data["Basic"]["Permission"]["Admin"].append(int(data))
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain(f"添加成功!")]
            ))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain(f"请检查语法！")]
            ))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def clear(
        app: Ariadne,
        group: Group,
        member: Member,
        saying: MessageChain
):
    if wake_check(saying.asDisplay(), readme.functions["clear"]["keys"]) and member.id in admins():
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain("\n"*40)]
        ))
