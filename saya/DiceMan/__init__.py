import random

from graia.saya import Saya, Channel
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Dice

from tool.callcheck import wake_check
from saya import Including

# Self-Including
readme = Including(author=None, group="游戏功能", functions={
            "Dice": {
                "describe": "今日人品",
                "show": True,
                "keys": [
                    "_骰子",
                    "随机骰子",
                    "_色子",
                    "随机色子"
                ]}
        })


saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def dice(app: Ariadne, group: Group, message: MessageChain):
    if wake_check(message.asDisplay().strip(), readme.functions["Dice"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([Dice(random.randint(1, 6))]))


