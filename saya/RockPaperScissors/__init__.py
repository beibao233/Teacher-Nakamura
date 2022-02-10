from graia.saya import Saya, Channel
from graia.ariadne.model import Member
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, At

from tool.callcheck import wake_check_var
from saya.CheckInControl import getCheckinList, checkInAction
from saya import Including

import random

# Self-Including
readme = Including(author=None, group="游戏功能", functions={
            "rps": {
                "describe": "石头剪刀布\n(剪刀，石头，布)",
                "show": True,
                "keys": [
                    "rps",
                    "stb",
                    "石头剪刀布"
                ]
            }
        })

saya = Saya.current()
channel = Channel.current()

name = {1: "石头", 2: "剪刀", 3: "布"}

situation = {1: 3, 2: 1, 3: 2}

rockText = ["石头", "ROCK", "STONE", "拳头", "FIST", "石", "ROCKS"]
scissorText = ["剪刀", "SCISSOR", "剪子", "王麻子", "SCISSORS"]
paperText = ["布", "CLOTH", "纸", "PAPER"]


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def rock_paper_scissor(app: Ariadne, group: Group, message: MessageChain, member: Member):
    result = wake_check_var(message.asDisplay().strip(), readme.functions["rps"]["keys"])
    if result is not False:
        if member.id in getCheckinList() and getCheckinList()[member.id]['num'] >= 1:

            checkInAction("delete", member.id, 1)

            formated_result = result.upper().strip()

            if formated_result in rockText:
                result = 1
            elif formated_result in scissorText:
                result = 2
            elif formated_result in paperText:
                result = 3
            else:
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain("您能说的更清楚点嘛？或者您可以用在帮助中的标准来和我对话！\n已经为您消耗一次签到！")
                ]))

            random_seed = random.randint(1, 3)

            if situation[random_seed] == result:
                checkInAction("add", member.id, 2)
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain(f"我出的是{name[random_seed]}... 我输了！\n你的两次签到已经给你了...")
                ]))
            elif random_seed == result:
                checkInAction("add", member.id, 1)
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain(f"我出的是{name[random_seed]}。 平局！\n你的一次签到还给你！")
                ]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain(f"我赢了！我出的是{name[random_seed]}！\n你的签到我就拿走啦~")
                ]))

        else:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain("你没有足够的签到次数\n尝试.ci后再来吧~")
            ]))
