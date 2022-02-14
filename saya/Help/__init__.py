from graia.saya import Saya, Channel
from graia.ariadne.model import Member
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage, Friend, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, At

from tool.callcheck import wake_check
from config.BFM_config import yaml_data
from saya import Including
from saya.ManagementControl import admins

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


def secondly_genereator(msg_start: str, gs ,show: bool=False):
    for _ in yaml_data["Saya"][gs]['Functions']:
        if yaml_data["Saya"][gs]['Functions'][_]["show"] or show:
            if yaml_data["Saya"][gs]['Functions'][_]["keys"][0].startswith("_"):
                if yaml_data["Saya"][gs]['Functions'][_]["keys"][0] == "_AT":
                    msg_start += f"\n@{yaml_data['Basic']['BotName']}: " + \
                                 yaml_data["Saya"][gs]['Functions'][_]["describe"]
                else:
                    msg_start += "\n" + \
                                 yaml_data["Saya"][gs]['Functions'][_]["keys"][0].replace("_", "") + ": " + \
                                 yaml_data["Saya"][gs]['Functions'][_]["describe"]
            else:
                msg_start += "\n" + yaml_data["Basic"]["WakeText"][0] + \
                             yaml_data["Saya"][gs]['Functions'][_]["keys"][0] + ": " + \
                             yaml_data["Saya"][gs]['Functions'][_]["describe"]
    return msg_start


def main_genereator(groups: dict, black_groups=None, msg_start="帮助列表:", show=False, full=False):
    if black_groups is None:
        black_groups = []

    for _ in groups:
        if not (_ in black_groups):
            if full is True:
                msg_start += f"\n————{_}————"
                for gs in groups[_]:
                    msg_start = secondly_genereator(msg_start=msg_start, gs=gs, show=show)
            else:
                if _ in ["角色功能", "人品功能", "游戏功能"]:
                    msg_start += f"\n————{_}————"
                    for gs in groups[_]:
                        msg_start = secondly_genereator(msg_start=msg_start, gs=gs, show=show)
    if full is not True:
        msg_start += "\n更多功能请加好友问我吧~"

    return msg_start


def help_msg(permid: int, where="Group", groups=None):
    if groups is None:
        groups = {}

    for _ in yaml_data["Saya"].keys():
        if yaml_data["Saya"][_]["Group"] in groups:
            groups[yaml_data["Saya"][_]["Group"]].append(_)
        else:
            groups[yaml_data["Saya"][_]["Group"]] = [_]

    if not (permid in admins()):
        message = main_genereator(groups=groups, black_groups=["后端功能", "管理功能"])
    elif where != "FRIEND":
        message = main_genereator(groups=groups)
    elif where == "FRIEND":
        message = main_genereator(groups=groups, full=True)
    else:
        message = main_genereator(groups=groups, show=True)
    return message


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def help_handler(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if wake_check(message.asDisplay().strip(), readme.functions["help"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain(f"\n" + help_msg(member.id))]
        ))


@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def help_handler(app: Ariadne, friend: Friend, message: MessageChain):
    if wake_check(message.asDisplay().strip(), readme.functions["help"]["keys"]):
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(help_msg(friend.id, where="FRIEND"))]
        ))
