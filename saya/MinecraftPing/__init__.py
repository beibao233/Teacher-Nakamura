from graia.saya import Saya, Channel
from graia.ariadne.model import Group
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.app import Ariadne

from saya import Including
from tool.callcheck import wake_check_var, wake_check
from .mcping import mcping

saya = Saya.current()
channel = Channel.current()

# Warning! 此插件为其他作者所写 本作者未经过同意复制并更改 如有版权请求我会立即删除
# Self-Including
readme = Including(author="A60", group="基础功能", functions={
    "mcping": {
        "describe": "获取MC服务器信息",
        "show": True,
        "keys": [
            "MC",
            "mc"
        ]
    }
})


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def minecraft_ping(app: Ariadne, group: Group, message: MessageChain):
    if wake_check_var(message.asDisplay().strip(), readme.functions["mcping"]["keys"]):
        saying = message.asDisplay().split()
        if len(saying) == 2:
            send_msg = await mcping(saying[1])
            await app.sendGroupMessage(str(group.id), MessageChain.create(send_msg))
    elif wake_check(message.asDisplay().strip(), readme.functions["mcping"]["keys"]):
        send_msg = await mcping("127.0.0.1:25565")
        await app.sendGroupMessage(str(group.id), MessageChain.create(send_msg))
