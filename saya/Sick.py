from graia.application.message.parser.literature import Literature
from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import Group, GroupMessage
from graia.application.message.elements.internal import Plain, MessageChain

from tool.callcheck import wake_check
from tool.qqname import isaqqnum
import random

# Self-Including
_author = None
_group = "基础功能"
_functions = {
    "sick": {
        "describe": "发送不寻常的信息",
        "show": True,
        "keys": [
            "犯病",
            "fb",
            "嘿嘿"
        ]
    }
}

saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def sick(
        app: GraiaMiraiApplication,
        group: Group,
        saying: MessageChain
):
    if wake_check(saying.asDisplay(), _functions["sick"]["keys"]):
        name = isaqqnum(saying.asDisplay())
        if not name:
            msg = "{0}你怎么样，我最近过的不好{1}。".format(saying.asDisplay().strip(), "5" * random.randint(0, 10))
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(f"" + msg * random.randint(1, 5))]
            ))
        else:
            msg = "{0}你怎么样，我最近过的不好{1}。".format(name, "5" * random.randint(0, 10))
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(f"" + msg * random.randint(1, 5))]
            ))
