from graia.saya import Saya, Channel
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain


from config.BFM_config import yaml_data

from .mcping import mcping
from tool.callcheck import wake_check
from saya import Including

saya = Saya.current()
channel = Channel.current()

# Self-Including
readme = Including(author="djkcyl", group="基础功能", functions={
            "mcping": {
                "describe": "获取MC服务器信息",
                "show": True,
                "keys": [
                    "MC",
                    "mc",
                    "mcping"
                ]
            }
        })


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def minecraft_ping(app: Ariadne, group: Group, message: MessageChain):
    if wake_check(message.asDisplay().strip(), readme.functions["mcping"]["keys"]):
        saying = message.asDisplay().split()
        if len(saying) == 2:
                send_msg = await mcping(saying[1])
                await app.sendGroupMessage(group.id, MessageChain.create(send_msg))
        else:
            await app.sendGroupMessage(group.id, MessageChain.create([Plain("用法：.mcping 服务器地址")]))
